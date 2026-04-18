import streamlit as st
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", 'src'))

from src.bm25 import BM25
from src.utils import *
#from src.rag_pipeline import get_retrievers, get_llm_prompt, lcel_pipeline
from src.rag_pipeline import get_retrievers, lcel_pipeline
#import src.rag_pipeline
#print(dir(src.rag_pipeline))

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from src.prompt import build_prompt


#Adopted from GPT. 

# --- 1. Load Retrievers ---
@st.cache_resource
def load_resources():
    return get_retrievers(3)
bm25_retriever, semantic_retriever, hybrid_retriever=load_resources()

# --- 2. UI Layout ---
st.title("Product Search")

query = st.text_input("What are you looking for?", placeholder="e.g., waterproof hiking boots")

# --- 3. Retrieval Logic ---
def get_results(query, mode, k=3):
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
def get_llm_prompt(): 
    # llm = OllamaLLM(
    #     model="qwen3.5:2b",
    #     model_kwargs={
    #         "repeat_penalty": 1.15,
    #         "temperature": 0.7,
    #         "top_p": 0.8
    #     }
    # )

    #Adopted from Gemini
    model_id = "./qwen3.5-0.8b"  # Ensure this points to your folder

    # # 1. Load the tokenizer and model using Transformers
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",      # This handles your Mac's GPU/MPS automatically
        torch_dtype="auto"
    )
    
    # # 2. Create a Transformers pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.8,
        repetition_penalty=1.15
    )
    
    # # 3. Wrap it for LangChain
    llm = HuggingFacePipeline(pipeline=pipe)

    prompt_template = build_prompt()
    return llm, prompt_template

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
                    # Truncate text to ~200 chars
                    #display_text = res['text'][:200] + "..." if len(res['text']) > 200 else res['text']
                    #st.write(display_text)
                with col2:
                    #st.metric("Score", res['score'])
                    st.write("⭐" * int(float(res['rating'])))
    with tab_rag:
        llm, prompt_template=get_llm_prompt()
        response = lcel_pipeline(query, hybrid_retriever, llm, prompt_template)
        st.info(response)