# Asked GPT: a list of statements to import
import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableParallel, RunnablePassthrough  
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
#from langchain_ollama import OllamaLLM
from langchain_community.llms import LlamaCpp
from prompt import build_prompt

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from langchain_community.retrievers import BM25Retriever
from hybrid import *

def get_retriever(vectorstore, query):
    # Adopted from Milestone 2 spec.
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5} # Fetch 5 most similar documents
    )

def build_context(docs):
    return "\n\n".join(
        f"Product ASIN: {doc.metadata.get('parent_asin', 'N/A')}\n"
        f"Title: {doc.metadata.get('product_title', '')}\n"
        f"Rating: {doc.metadata['rating']}/5]\n"
        f"Features: {doc.metadata['features']}]\n"
        f"Description: {doc.metadata['description']}]\n"
        f"Price: {doc.metadata['price']}]\n"
        f"Categories: {doc.metadata['categories']}]\n"
        for doc in docs
    )

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

if __name__ == '__main__':
    query = "What is the best rated skateboard?"
    merged_df = pd.read_csv('data/processed/merged.csv')
    data_dicts = merged_df.to_dict(orient="records")
    documents = list()
    for record in data_dicts:
        data = record.pop("full_content").split('|')
        record['product_title'] = data[0]
        record['rating'] = data[1]
        record['features'] = data[2]
        record['description'] = data[3]
        record['price'] = data[4]
        record['categories'] = data[5]
        reviews='\n'.join(data[6:])
        doc = Document(
            page_content=reviews, # Remove this key 
            metadata=record # Use the 'parent_asin' entry as metadata
        )
        documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    split_docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    hybrid_retriever=hybrid_RAG(split_docs, vectorstore)

    retriever = get_retriever(vectorstore, query)
    #llm = OllamaLLM(
    #    model="qwen3.5:2b",
    # llm = Llama(
    #     model="qwen3.5-0.8b",
    #     model_kwargs={
    #         "repeat_penalty": 1.15,
    #         "temperature": 0.7,
    #         "top_p": 0.8
    #     }
    # )

    #Adopted from Gemini
    model_id = "./qwen3.5-0.8b"  # Ensure this points to your folder

    # 1. Load the tokenizer and model using Transformers
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",      # This handles your Mac's GPU/MPS automatically
        torch_dtype="auto"
    )
    
    # 2. Create a Transformers pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.8,
        repetition_penalty=1.15
    )
    
    # 3. Wrap it for LangChain
    llm = HuggingFacePipeline(pipeline=pipe)
    
    print('Semantic retriever: \n', lcel_pipeline(query, retriever, llm, build_prompt()))
    print('Hybrid retriever: \n', lcel_pipeline(query, hybrid_retriever, llm, build_prompt()))