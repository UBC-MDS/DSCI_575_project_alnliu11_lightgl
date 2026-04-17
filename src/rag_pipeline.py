from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough  
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from pathlib import Path
from prompt import build_prompt
from utils import construct_corpus
from semantic import build_embeddings, get_vector_store

def get_retriever(vectorstore):
    # Adopted from Milestone 2 spec.
    print("Getting retriever...")
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5} # Fetch 5 most similar documents
    )

def build_context(docs):
    context_parts = list()
    for doc in docs:
        # Asked GPT something like: How can LLM interpret query like "Find me this kind of product under $15"?
        # Deal with missing price
        p = doc.metadata.get("price", -1.0)
        price_display = f"${p:.2f}" if p > 0 else "Price not available"

        r = doc.metadata.get("average_rating", -1.0)
        rating_display = f"{r}/5" if r > 0 else "Rating not available"
        
        # Provide alternative values in case previous preprocessing falls through
        asin = doc.metadata.get('parent_asin', 'N/A')
        title = doc.metadata.get('title', 'No Title Provided')
        features = doc.metadata.get('features', 'No features listed')
        desc = doc.metadata.get('description', 'No description available')
        cats = doc.metadata.get('categories', 'N/A')

        item_str = (
            f"Product ASIN: {asin}\n"
            f"Product Title: {title}\n"
            f"Rating: {rating_display}/5\n"
            f"Features: {features}\n"
            f"Description: {desc}\n"
            f"Price: {price_display}\n"
            f"Categories: {cats}"
        )
        context_parts.append(item_str)

    return "\n\n---\n\n".join(context_parts)

def lcel_pipeline(query: str, 
    retriever: BaseRetriever, 
    llm: BaseChatModel, 
    prompt_template: ChatPromptTemplate
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
            "context": retriever | build_context,
            "question": RunnablePassthrough()
        })
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(query)

def run_query_loop(retriever: BaseRetriever, llm: BaseChatModel, prompt_template: ChatPromptTemplate):
    print("Enter a query, or type 'exit' / 'quit' / press Enter on an empty line to stop.")
    while True:
        try:
            query = input("Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nStopping query loop.")
            break

        if not query or query.lower() in {"exit", "quit"}:
            print("Stopping query loop.")
            break

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
    vector_store = get_vector_store(
        embeddings=embeddings,
        faiss_index_dir=faiss_index_dir,
        corpus_builder=lambda: construct_corpus(
            text_splitter=text_splitter,
            threshold=20000
        )
    )
    retriever = get_retriever(vector_store)
    llm = OllamaLLM(
        model="qwen3.5:2b",
        model_kwargs={
            "repeat_penalty": 1.15,
            "temperature": 0.7,
            "top_p": 0.8
        }
    )
    prompt_template = build_prompt()
    # Asked GPT: How to enable user to keep specifying query until they are done?
    run_query_loop(retriever, llm, prompt_template)