from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from utils import *

def get_product_list(): 
    merged_df=pd.read_csv('data/processed/merged.csv')
    products=merged_df.loc[:, 'full_content']
    products=products.tolist()
    return products

def save_index(embeddings, products, faiss_index_dir): 
    vector_store = FAISS.from_texts(products, embeddings)
    vector_store.save_local(faiss_index_dir)

def get_query_results(queries): 
    semantic_search_results=[]
    for q in queries: 
        semantic_search_results.append(vector_store.similarity_search(q, k=5))
    return semantic_search_results

if __name__ == '__main__':
    products=get_product_list()

    #Adopted from GPT. 
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    faiss_index_dir="faiss_index"
    save_index(embeddings, products, faiss_index_dir)

    #Adopted from GPT. 
    vector_store = FAISS.load_local(
        faiss_index_dir,
        embeddings,
        allow_dangerous_deserialization=True
    )

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
    semantic_search_results=get_query_results(queries)
    print(semantic_search_results)