import streamlit as st
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import *
from src.rag_pipeline import get_retrievers, lcel_pipeline, get_llm_prompt

from src.download_data import main

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from src.prompt import build_prompt

api_key = os.getenv("GROQ_API_KEY")


#Adopted from GPT. 

# --- 1. Load Retrievers ---
@st.cache_resource
def load_resources():
    """
    Download Amazon products and review data. Return BM25Retriever, VectorStoreRetriever, and EnsembleRetriever.
    The first two retrieves 3 documents max, and the last one retrieves 6 max.

    Parameters
    ----------
    None

    Returns
    -------
    tuple
        tuple of three elements, which are BM25Retriever, VectorStoreRetriever, and EnsembleRetriever.
    """
    main()
    return get_retrievers(3)
bm25_retriever, semantic_retriever, hybrid_retriever=load_resources()

# --- 2. UI Layout ---
st.title("Product Search")

query = st.text_input("What are you looking for?", placeholder="e.g., waterproof hiking boots")

# --- 3. Retrieval Logic ---
def get_results(query, mode, k=3):
    """
    Use the retrieve corresponding to the given mode to search documents.
    Return the title and rating of a maximum of top k documents.

    Parameters
    ----------
    query : str
        user query.
    mode : str
        either "BM25", "Semantic", or "Hybrid" mode.
    k : int
        number of documents to retrieve.

    Returns
    -------
    list of dict
        a list of dict of top k documents' title and rating.
    """
    results = []
    
    if mode == "BM25":
        docs=bm25_retriever.invoke(query)

    elif mode == "Semantic":
        docs=semantic_retriever.invoke(query)
    elif search_mode == "Hybrid": 
        docs = hybrid_retriever.invoke(query)
    for doc in docs[:k]: 
        title = doc.metadata.get('title', 'No Title Provided')
        rating = doc.metadata.get("average_rating", -1.0)
        results.append({"title": title, "rating": rating})

    return results

@st.cache_resource
def get_llm_prompt_cached():
    """
    A cached version of rag_pipeline.py `get_llm_prompt()`

    Parameters
    ----------
    None

    Returns
    -------
    tuple
        tuple of two elements. LLM and prompt.
    """
    return get_llm_prompt("llama-3.1-8b-instant")

# --- 4. Display ---
if query:
    tab_search, tab_rag = st.tabs(["Search Only", "RAG Mode"])

    with tab_search:
        search_mode = st.radio("Search Mode", ["BM25", "Semantic", "Hybrid"], horizontal=True)

        st.subheader(f"Top 3 {search_mode} Results")

        search_results = get_results(query, search_mode)
        
        for res in search_results:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{res['title']}**")
                with col2:
                    st.write("⭐" * int(float(res['rating'])))
    with tab_rag:
        llm, prompt_template=get_llm_prompt_cached()
        response = lcel_pipeline(query, hybrid_retriever, llm, prompt_template)
        st.info(response)