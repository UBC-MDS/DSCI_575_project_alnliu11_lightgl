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

    queries=['wireless bluetooth headphones', 
         'headphones that block airplane noise', 
         'best headphones for long flights under $200', 
         'stainless steel water bottle 1 liter', 
         'something to keep water cold all day', 
         'what’s the best water bottle for hiking in hot weather', 
         'kids lego star wars set', 
         'toy for a child who likes space battles', 
         'what is a good educational toy for a 7-year-old interested in space', 
         'shoes'
    ]
    semantic_search_results=get_query_results(queries)
    print(semantic_search_results)