from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

def hybrid_RAG(docs, vectorstore): 
    bm25_retriever = BM25Retriever.from_documents(
            docs,  # docs is a Langchain Document objects
            k=5    # returns top 5 results
            )
    # Initialize individual retrievers
    vector_retriever = vectorstore.as_retriever()

    # Create the ensemble
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6]  # Example: asigning 40% importance to BM25, 60% to Semantic Search
    )

    # Invoke to get combined results
    #docs = ensemble_retriever.invoke(query)

    return ensemble_retriever