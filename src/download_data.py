import os
import requests
import zipfile
import io

def download_dataset():
    url = "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    print(f"Downloading dataset from {url}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(data_dir)
        print("Dataset extracted successfully to 'data/' directory.")
    else:
        print(f"Failed to download dataset. Status code: {response.status_code}")

if __name__ == "__main__":
    download_dataset()
