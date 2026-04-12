import requests
import sys
import os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

data_folder = Path("data/raw")
data_folder.mkdir(parents=True, exist_ok=True)

# Asked Gemini how to download data from link to jsonl.gz
def download_data(url, file_name):
    save_path = data_folder / file_name

    if save_path.exists():
        print(f"File Already exists at: {save_path}")
        return
    
    print(f"Downloading to: {save_path}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("Download complete!")

def main():
    """Downloads data from the web to a local filepath."""
    data_folder = Path("data/raw")
    data_folder.mkdir(parents=True, exist_ok=True)

    # download review data
    url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Sports_and_Outdoors.jsonl.gz"
    file_name = "Sports_and_Outdoors.jsonl.gz"
    download_data(url, file_name)

    # download meta data
    url = "https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_Sports_and_Outdoors.jsonl.gz"
    file_name = "meta_Sports_and_Outdoors.jsonl.gz"
    download_data(url, file_name)



if __name__ == "__main__":
    main()