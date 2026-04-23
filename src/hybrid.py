from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

def hybrid_RAG(bm25_retriever, semantics_retriever, weights=[0.3, 0.7]):
    """
    Return a EnsembleRetriever

    Parameters
    ----------
    bm25_retriever : BM25Retriever
        retriever based on BM25 keyword search.
    semantics_retriever : VectorStoreRetriever
        retriever based on text vectors.

    weights : list of float
        a list of two elements that refer to the weights
        for the BM25 retriever and Semantics retriever.

    Returns
    -------
    langchain_classic.retrievers.EnsembleRetriever
        ensemble retriever that combines results of both the
        given retrievers with the given weights.
    """
    # Create the ensemble
    print("Creating Ensemble Retriever...")
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, semantics_retriever],
        weights=weights
    )

    return ensemble_retriever