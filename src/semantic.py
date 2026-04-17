from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils import *

def get_vector_store(embeddings, faiss_index_dir, documents=None, corpus_builder=None):
    #Adopted from GPT.
    vector_store = None
    if faiss_index_dir.exists():
        print("Loading FAISS Index...")
        vector_store = FAISS.load_local(
            faiss_index_dir,
            embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        if documents is None:
            if corpus_builder is None:
                raise ValueError("Provide either `documents` or `corpus_builder`.")
            documents = corpus_builder()
        print("Creating FAISS Index...")
        vector_store = FAISS.from_documents(documents, embeddings)
        print("Saving...")
        vector_store.save_local(faiss_index_dir)
        print("Done!")
    return vector_store

def get_query_results(queries, vector_store): 
    semantic_search_results=[]
    for q in queries: 
        semantic_search_results.append(vector_store.similarity_search(q, k=5))
    return semantic_search_results