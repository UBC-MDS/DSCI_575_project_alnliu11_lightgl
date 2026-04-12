from langchain_community.retrievers import BM25Retriever
import joblib

class BM25:
    def __init__(self, retriever):
        self.retriever = retriever
    
    @classmethod
    def from_documents(cls, docs, k, func):
        retriever = BM25Retriever.from_documents(
            docs,
            k=k,
            preprocess_func=func,
        )
        return cls(retriever)

    @classmethod
    def from_index(cls, path):
        retriever = joblib.load(path)
        return cls(retriever)
            
    def retrieve(self, query):
        return self.retriever.invoke(query)
    
    def dump_index(self, path):
        return joblib.dump(self.retriever, path)