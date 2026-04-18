from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

def hybrid_RAG(bm25_retriever, semantics_retriever):
    # Create the ensemble
    print("Creating Ensemble Retriever...")
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, semantics_retriever],
        weights=[0.3, 0.7]  # Example: asigning 40% importance to BM25, 60% to Semantic Search
    )

    return ensemble_retriever