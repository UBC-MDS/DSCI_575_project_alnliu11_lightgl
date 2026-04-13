import streamlit as st
import pandas as pd
from rank_bm25 import BM25Okapi
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.bm25 import BM25
from src.utils import *

#Adopted from GPT. 

# --- 1. Load Data & Models ---
@st.cache_resource
def load_resources():
    # Load your embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load your existing FAISS index (allow_dangerous_deserialization for local pkl)
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Extract metadata/text for BM25
    content = [doc.page_content for doc in vector_store.docstore._dict.values()]

    docs = construct_corpus()
    bm25 = BM25.from_documents(docs, 3, preprocess_and_tokenize)
    
    return vector_store, bm25, content

vector_store, bm25, all_texts = load_resources()

# --- 2. UI Layout ---
st.title("Product Review Search")

search_mode = st.radio("Search Mode", ["BM25", "Semantic", "Hybrid"], horizontal=True)
query = st.text_input("What are you looking for?", placeholder="e.g., waterproof hiking boots")

# --- 3. Retrieval Logic ---
def get_results(query, mode, k=3):
    results = []
    
    if mode == "BM25":
        tokenized_query = preprocess_and_tokenize(query)
        scores = bm25.retriever.vectorizer.get_scores(tokenized_query)
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        for i in top_n:
            title=all_texts[i].split('|')[0]
            rating=all_texts[i].split('|')[1]
            reviews='\n'.join(all_texts[i].split('|')[6:])
            results.append({"text": reviews, "score": round(scores[i], 4), "title": title, "rating": rating})

    elif mode == "Semantic":
        docs_and_scores = vector_store.similarity_search_with_score(query, k=k)
        for doc, score in docs_and_scores:
            title=doc.page_content.split('|')[0]
            rating=doc.page_content.split('|')[1]
            reviews='\n'.join(doc.page_content.split('|')[6:])
            # Note: FAISS score is L2 distance (lower is better)
            results.append({"text": reviews, "score": round(float(score), 4), "title": title, "rating": rating})
            
    return results

# --- 4. Display ---
if query:
    st.subheader(f"Top 3 {search_mode} Results")
    if search_mode == "Hybrid": 
        search_results = get_results(query, 'BM25', 1) + get_results(query, 'Semantic', 2)
    else: 
        search_results = get_results(query, search_mode)
    
    for res in search_results:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{res['title']}**")
                # Truncate text to ~200 chars
                display_text = res['text'][:200] + "..." if len(res['text']) > 200 else res['text']
                st.write(display_text)
            with col2:
                st.metric("Score", res['score'])
                st.write("⭐" * int(float(res['rating'])))