from utils import *
from bm25 import BM25

if __name__ == '__main__':
    docs = construct_corpus()
    bm25_model = BM25.from_documents(docs, 5, preprocess_and_tokenize)
    print(bm25_model.retrieve("Wheels"))