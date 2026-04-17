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
from langchain_ollama import OllamaLLM
from pathlib import Path
from prompt import build_prompt
from utils import construct_corpus
from semantic import get_vector_store

def get_retriever(vectorstore, query):
    # Adopted from Milestone 2 spec.
    print("Getting retriever...")
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

if __name__ == '__main__':
    query = "What is the best rated skateboard?"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    print("Getting embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index_dir = Path("models/faiss_index")
    # Asked GPT: how to adjust the script to only construct corpus if we do not have the FAISS index?
    vector_store = get_vector_store(
        embeddings=embeddings,
        faiss_index_dir=faiss_index_dir,
        corpus_builder=lambda: construct_corpus(text_splitter)
    )
    retriever = get_retriever(vector_store, query)
    llm = OllamaLLM(
        model="qwen3.5:2b",
        model_kwargs={
            "repeat_penalty": 1.15,
            "temperature": 0.7,
            "top_p": 0.8
        }
    )
    print(lcel_pipeline(query, retriever, llm, build_prompt()))