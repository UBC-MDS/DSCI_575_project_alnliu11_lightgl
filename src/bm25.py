from langchain_community.retrievers import BM25Retriever
import joblib

class BM25:
    def __init__(self, retriever):
        self.retriever = retriever
    
    @classmethod
    def from_documents(cls, docs, k, func, save_path):
        retriever = BM25Retriever.from_documents(
            docs,
            k=k,
            preprocess_func=func,
        )
        dump_index(save_path)
        return cls(retriever)

    @classmethod
    # def from_index(cls, path, docs, k, func):
    #     if path.exists():
    #         print("Loading BM25 Index...")
    #         retriever = joblib.load(path)
    #     else:
    #         retriever = from_documents(cls, docs, k, func).retriever
    #         dump_index(path)
    #     return cls(retriever)
    def from_index(cls, path):
        retriever = joblib.load(path)
        return cls(retriever)
            
    def retrieve(self, query):
        return self.retriever.invoke(query)
    
    def retrieve_with_scores(self, query, k=5):
        # Asked GitHub Copilot how to retrieve the top 5 results with scores.
        query_tokens = self.retriever.preprocess_func(query)
        scores = self.retriever.vectorizer.get_scores(query_tokens)
        docs = self.retriever.docs
        # Find the index of the top k highest scores
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        # Return a list of documents with corresponding scores
        return [
            {"doc": docs[i], "score": float(scores[i])}
            for i in top_idx
        ]
    
    def dump_index(self, path):
        return joblib.dump(self.retriever, path)