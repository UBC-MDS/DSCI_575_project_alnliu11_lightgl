import pandas as pd
import string
import gzip
import json
import os
import sys
import nltk
from pathlib import Path
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from langchain_core.documents import Document
from collections import Counter

nltk.download("punkt_tab")
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stop_words.update(string.punctuation)
stop_words.update(['``', '’', '`', 'br', '"', '”', "''", "'s"])

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

data_folder = Path("data/raw")
data_folder.mkdir(parents=True, exist_ok=True)

processed_data_folder = Path("data/processed")
processed_data_folder.mkdir(parents=True, exist_ok=True)
processed_data_path = processed_data_folder / "merged.csv"

def remove_unwanted_keys(unwanted_keys, data):
    for key in unwanted_keys:
        data.pop(key, None)

def assemble_product_info(threshold = 20000):
    product_count = 1
    product_list = list()
    parent_asin_set = set()
    unwanted_keys = ['main_category', 'rating_number', 'images', 'videos', 'store', 'details', 'bought_together', 'subtitle', 'author']
    merged_keys = ['title', 'average_rating', 'features', 'description', 'price', 'categories']
    # Gemini's approach to reading .jsonl.gz without unzipping
    meta_path = data_folder / "meta_Sports_and_Outdoors.jsonl.gz"
    with gzip.open(meta_path, 'rt', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)

            # Remove unwanted keys
            remove_unwanted_keys(unwanted_keys, data)

            # Combine list into one text
            data['features'] = ' '.join(data['features'])
            data['description'] = ' '.join(data['description'])
            data['categories'] = ' '.join(data['categories'])

            # Add to product
            product_list.append(data)
            parent_asin_set.add(data['parent_asin'])

            # Check with threshold
            product_count += 1
            
            if product_count >= threshold:
                break
            elif product_count % 5000 == 0:
                print(f"Processing Product #{product_count}")

    # Fixed Columns with Nulls or empty strings
    product_df = pd.DataFrame(product_list)
    print("Fixing Null Values...")
    null_columns = ['features', 'description', 'categories']
    for col in null_columns:
        product_df.loc[:, col] = product_df.loc[:, col].fillna("Missing")
        product_df.loc[product_df[col] == '', col] = "Missing"
    product_df['price'] = product_df['price'].fillna(-1.0).astype(float)

    return product_df, parent_asin_set

def assemble_reviews_info(parent_asin_set, threshold = 20):
    # Identify the corresponding review data
    asin_reviews_count = Counter()
    review_count = 1
    review_path = data_folder / "Sports_and_Outdoors.jsonl.gz"
    review_list = list()
    unwanted_keys = ['rating', 'images', 'images', 'asin', 'user_id', 'timestamp', 'helpful_vote', 'verified_purchase']
    merged_keys = ['title', 'text']

    with gzip.open(review_path, 'rt', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # Check if desired parent_asin
            parent_asin = data.get("parent_asin")
            if parent_asin not in parent_asin_set:
                continue
            elif asin_reviews_count[parent_asin] == threshold:
                # Control at the threshold # of reviews
                continue

            # Remove unwanted keys
            remove_unwanted_keys(unwanted_keys, data)

            # Merge all contents
            parts = [str(data.get(k, "")) for k in merged_keys]
            data["review"] = " | ".join(parts)
            remove_unwanted_keys(merged_keys, data)

            # Add to product
            review_list.append(data)
            review_count += 1
            asin_reviews_count[parent_asin] += 1

            if review_count % 10000 == 0:
                print(f"Processing Review #{review_count}")
    
    reviews_df = pd.DataFrame(review_list)
    # Asked Gemini: How to group by the same key in dataframe and concatenate the all the strings in one column?
    reviews_df = reviews_df.groupby("parent_asin")["review"].agg(" | ".join).reset_index()
    print(f"Length of reviews_df: {len(reviews_df)}")
    print("Top 5 lines:")
    print(reviews_df.head())
    return reviews_df

def merge_product_and_reviews(threshold = 20000):
    print("Getting Product Info...")
    products_df, parent_asin_set = assemble_product_info(threshold)
    print("Getting Reviews Info...")
    reviews_df = assemble_reviews_info(parent_asin_set)
    print("Merging...")
    merged_df = pd.merge(products_df, reviews_df, on='parent_asin', how='inner')
    merged_df.to_csv(processed_data_folder / "merged.csv")
    print("Done!")

def construct_corpus(text_splitter=None, threshold = 20000):
    # Create Merged data if not existent
    if not processed_data_path.exists():
        merge_product_and_reviews(threshold=threshold)
    merged_df = pd.read_csv(processed_data_path, index_col=0)
    
    # Create corpus
    print("Constructing corpus...")
    data_dicts = merged_df.to_dict(orient="records")
    docs = [
        Document(
            page_content=record.pop("review"), # Remove this key 
            metadata=record # Use the 'parent_asin' entry as metadata
        ) 
        for record in data_dicts
    ]
    if text_splitter is not None:
        print("Splitting Docs...")
        docs = text_splitter.split_documents(docs)

    print("Done!")
    return docs

def preprocess_and_tokenize(text):
    """
    Adapted from DSCI_563_Lab_3 by Hedayat Zarkoob. (https://github.ubc.ca/mds-2025-26/DSCI_563_unsup-learn_students/blob/master/labs/lab3/student/preprocessing.py)
    Made available under Attribution 4.0 International (CC BY 4.0).
    Use nltk `sent_tokenize` to split sentences and `word_tokenize` to split words.
    Lowercase words and ignore stop words.
    Return tokens in list.
    """ 
    sentences = sent_tokenize(text)
    preprocessed = list()
    for sent in sentences: 
        tokenized = word_tokenize(sent)
        for token in tokenized:
            token = token.lower()
            if token not in stop_words:
                preprocessed.append(token)
    return preprocessed

if __name__ == '__main__':
    merge_product_and_reviews()
