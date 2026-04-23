import os
import time
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils import *


def _resolve_embedding_device(device=None):
    """
    Resolve the device for building text embeddings based on the user system, if specified "auto".

    Parameters
    ----------
    device : str
        device for building text embeddings.

    Returns
    -------
    string
        resolved device name.
    """
    requested_device = (device or os.getenv("EMBEDDINGS_DEVICE", "auto")).strip().lower()
    if requested_device == "auto":
        try:
            import torch

            return "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            return "cpu"

    return requested_device


def build_embeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", device=None):
    """
    Loading embeddings of the given model with the given device.

    Parameters
    ----------
    model_name : str
        embeddings model.
    device : str
        device for loading.

    Returns
    -------
    HuggingFaceEmbeddings
        the corresponding hugging face embeddings.
    """
    # Asked GPT: What to do to make the embeddings run on GPU,
    # while accommodating other developers who do not have GPU?
    resolved_device = _resolve_embedding_device(device)
    print(f"Loading embeddings on {resolved_device}...")
    # Asked GPT: How to use `time` to time a piece of code?
    start_time = time.perf_counter()
    model_kwargs = {"device": resolved_device} if resolved_device else {}
    embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
    execution_time = time.perf_counter() - start_time
    print(f"Embedding loading took {execution_time:.4f} seconds.")
    return embeddings


def get_vector_store(embeddings, faiss_index_dir, documents=None, corpus_builder=None):
    """
    Created and returned FAISS vector database generated with given embeddings. Saved the word vectors
    in the given directory. Either documents or corpus_builder should be passed. If given documents,
    built FAISS word vectors based on documents. If did not pass documents, generate documents with
    corpus_builder before building the word vectors.

    Parameters
    ----------
    embeddings : HuggingFaceEmbeddings
        the hugging face embeddings.
    faiss_index_dir : pathlib.Path
        directory path for saving FAISS vector database to.
    documents : Document
        documents to create the vector database from.
    corpus_builder : function
        function for building the documents, if documents not specified.

    Returns
    -------
    FAISS
        vector database generated with the given documents or documents built with corpus_builder.
    """
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
        # Asked GPT: How to use `time` to time a piece of code?
        start_time = time.perf_counter()
        vector_store = FAISS.from_documents(documents, embeddings)
        print("Saving...")
        vector_store.save_local(faiss_index_dir)
        execution_time = time.perf_counter() - start_time
        print(f"Creating FAISS Index took {execution_time:.4f} seconds.")
    return vector_store