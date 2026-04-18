from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda  
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_ollama import OllamaLLM
from pathlib import Path
from prompt import build_prompt
from utils import construct_corpus, preprocess_and_tokenize
from semantic import build_embeddings, get_vector_store

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import traceback

#from langchain_community.retrievers import BM25Retriever
from hybrid import hybrid_RAG
from bm25 import BM25

def get_retriever(vectorstore):
    # Adopted from Milestone 2 spec.
    print("Getting retriever...")
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

def build_context(docs):
    context_parts = list()
    print(len(docs))
    for doc in docs:
        # Provide alternative values in case previous preprocessing falls through
        asin = doc.metadata.get('parent_asin', 'N/A')
        title = doc.metadata.get('title', 'No Title Provided')
        reviews = doc.page_content

        # Asked GPT something like: How can LLM interpret query like "Find me this kind of product under $15"?
        # Deal with missing price
        p = doc.metadata.get("price", -1.0)
        price_display = f"${p:.2f}" if p > 0 else "Price not available"

        r = doc.metadata.get("average_rating", -1.0)
        rating_display = f"{r}/5" if r > 0 else "Rating not available"

        item_str = (
            f"Product ASIN: {asin}\n"
            f"Product Title: {title}\n"
            f"Rating: {rating_display}/5\n"
            f"Reviews: {reviews}\n"
            f"Price: {price_display}\n"
        )
        context_parts.append(item_str)

    return "\n\n---\n\n".join(context_parts)

def lcel_pipeline(query: str, 
    retriever: BaseRetriever, 
    llm: BaseChatModel, 
    prompt_template: ChatPromptTemplate,
    top_k=3
):
    # Asked GPT:
    # Suppose I want to wrap this as a function, can you show me a list of statements
    # to import and a list of arguments to pass in. Don't show me what the code for
    # individual functions, but show me what functions should be passed and
    # what each of them should do.
    # What are the types of each of these arguments?
    print("Running RAG Chain...")
    rag_chain = (
        RunnableParallel({
            "context": (retriever
                        | RunnableLambda(lambda docs: docs[:top_k])
                        | build_context
                        ),
            "question": RunnablePassthrough()
        })
        | prompt_template
        | llm
        | StrOutputParser()
    )
    try:
        response = rag_chain.invoke(query)
        if not response or not str(response).strip():
            print("[DEBUG] Chain completed but returned an empty response.")
        return response
    except Exception as exc:
        print(f"[DEBUG] RAG chain failed: {exc}")
        print(traceback.format_exc())
        raise


def debug_rag_once(
    query: str,
    retriever: BaseRetriever,
    llm,
    prompt_template: ChatPromptTemplate,
    max_docs_preview: int = 2,
):
    print("\n[DEBUG] Stage 1: Retrieve documents")
    docs = retriever.invoke(query)
    print(f"[DEBUG] Retrieved {len(docs)} documents.")
    for i, doc in enumerate(docs[:max_docs_preview], start=1):
        snippet = doc.page_content[:220].replace("\n", " ")
        print(f"[DEBUG] Doc {i} snippet: {snippet}")

    print("\n[DEBUG] Stage 2: Build context")
    context = build_context(docs)
    print(f"[DEBUG] Context length: {len(context)} characters")
    print(f"[DEBUG] Context preview: {context[:350]}")

    print("\n[DEBUG] Stage 3: Render prompt")
    prompt_value = prompt_template.invoke({"context": context, "question": query})
    prompt_text = prompt_value.to_string()
    print(f"[DEBUG] Prompt length: {len(prompt_text)} characters")
    print(f"[DEBUG] Prompt preview: {prompt_text[:500]}")

    print("\n[DEBUG] Stage 4: Full chain invoke")
    final_output = lcel_pipeline(query, retriever, llm, prompt_template)
    print(f"[DEBUG] Final output preview: {str(final_output)[:400]}")
    return final_output

def run_query_loop(retriever: BaseRetriever, llm: BaseChatModel, prompt_template: ChatPromptTemplate):
    print("Enter a query, or type 'exit' / 'quit' / press Enter on an empty line to stop.")
    print("Type '/debug <your query>' to print chain internals.")
    while True:
        try:
            query = input("Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nStopping query loop.")
            break

        if not query or query.lower() in {"exit", "quit"}:
            print("Stopping query loop.")
            break
        # Asked GPT how to debug the RAG chain process.
        if query.startswith("/debug "):
            debug_query = query[len("/debug "):].strip()
            if not debug_query:
                print("Provide a query after '/debug'.")
                continue
            response = debug_rag_once(debug_query, retriever, llm, prompt_template)
        else:
            response = lcel_pipeline(query, retriever, llm, prompt_template)
        print("\nResponse:\n")
        print(response)
        print("\n" + "=" * 80 + "\n")

if __name__ == '__main__':
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    embeddings = build_embeddings()
    faiss_index_dir = Path("models/faiss_index")
    # Asked GPT: how to adjust the script to only construct corpus if we do not have the FAISS index?
    docs = construct_corpus(
        text_splitter=text_splitter,
        threshold=20000
    )
    vector_store = get_vector_store(
        embeddings=embeddings,
        faiss_index_dir=faiss_index_dir,
        documents=docs
    )
    topK = 3
    bm25_index_dir = Path("models/bm25_index")
    bm25 = BM25.from_index_or_documents(docs, topK, preprocess_and_tokenize, bm25_index_dir)
    semantic_retriever = get_retriever(vector_store)
    hybrid_retriever = hybrid_RAG(bm25.retriever, semantic_retriever)

    llm = OllamaLLM(
        model="qwen3.5:2b",
        num_ctx=4096,
        model_kwargs={
            "repeat_penalty": 1.15,
            "temperature": 0.7,
            "top_p": 0.8
        }
    )

    #Adopted from Gemini
    # model_id = "./qwen3.5-0.8b"  # Ensure this points to your folder

    # # 1. Load the tokenizer and model using Transformers
    # tokenizer = AutoTokenizer.from_pretrained(model_id)
    # model = AutoModelForCausalLM.from_pretrained(
    #     model_id,
    #     device_map="auto",      # This handles your Mac's GPU/MPS automatically
    #     torch_dtype="auto"
    # )
    
    # # 2. Create a Transformers pipeline
    # pipe = pipeline(
    #     "text-generation",
    #     model=model,
    #     tokenizer=tokenizer,
    #     max_new_tokens=512,
    #     temperature=0.7,
    #     top_p=0.8,
    #     repetition_penalty=1.15
    # )
    
    # # 3. Wrap it for LangChain
    # llm_lite = HuggingFacePipeline(pipeline=pipe)

    prompt_template = build_prompt()
    # Asked GPT: How to enable user to keep specifying query until they are done?
    # print('\nSemantic retriever:\n')
    # run_query_loop(semantic_retriever, llm, prompt_template)

    print('\nHybrid retriever:\n')
    run_query_loop(hybrid_retriever, llm, prompt_template)
