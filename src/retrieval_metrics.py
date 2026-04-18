from utils import *
from bm25 import BM25
from semantic import get_vector_store
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

if __name__ == '__main__':
    topK=5
    docs = construct_corpus()
    bm25_index_dir=Path("models/bm25_index")
    bm25_model = BM25.from_documents(docs, topK, preprocess_and_tokenize, bm25_index_dir)

    queries=['yoga mat 6mm non-slip', 
             'something comfortable for floor stretching', 
             'what is the best portable yoga mat for a tall beginner on a budget', 
             'waterproof 2 person camping tent', 
             'shelter for a rainy weekend in the woods', 
             'lightweight tent for backpacking that can withstand high winds and heavy rain', 
             '20 lb adjustable dumbbells',
             'equipment for building arm strength at home',
             'what are the best compact weights for a small apartment gym for high-intensity training', 
             'carbon fiber road bike',
             'fast bicycle for paved surfaces',
             'what is a durable and lightweight bike suitable for long-distance commuting on hilly terrain'
            ]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    faiss_index_dir = Path("models/faiss_index")
    vector_store = get_vector_store(embeddings, faiss_index_dir, documents=docs)

    metrics=[]
    for q in queries[:5]: 
        semantic_results=vector_store.similarity_search(q, k=topK)
        bm25_results=bm25_model.retrieve(q)
        print(bm25_model.retrieve_with_scores(q))
        break
        for i in range(topK): 
            metrics.append({'Query': q, 'Semantic': semantic_results[i].page_content.split('|')[0], 'BM25': bm25_results[i].page_content.split('|')[0]})
    df_metrics = pd.DataFrame(metrics)

    results_folder = Path("results")
    results_folder.mkdir(parents=True, exist_ok=True)
    df_metrics.to_csv(results_folder/'metrics.csv')
    #print(bm25_model.retrieve("Wheels"))