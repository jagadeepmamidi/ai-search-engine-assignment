import os
from sklearn.datasets import fetch_20newsgroups
from src.config import DOCS_DIR
from src.embedder import EmbeddingModel
from src.search_engine import SearchEngine
import pickle

def prepare_data():
    # 1. Download Dataset
    print("Fetching dataset...")
    dataset = fetch_20newsgroups(subset='train', categories=['sci.space', 'sci.med', 'comp.graphics'], remove=('headers', 'footers', 'quotes'))
    
    docs_data = []
    
    # 2. Save to .txt (Simulating local file storage) & Prepare List
    for i, text in enumerate(dataset.data[:150]): # Limit to 150 docs
        if len(text) < 50: continue # Skip tiny docs
        
        doc_id = f"doc_{i:03d}"
        file_path = os.path.join(DOCS_DIR, f"{doc_id}.txt")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        docs_data.append({"doc_id": doc_id, "text": text})

    # 3. Generate Embeddings with Caching
    embedder = EmbeddingModel()
    embeddings = []
    valid_docs = []

    print("Generating Embeddings...")
    for doc in docs_data:
        emb = embedder.get_embedding(doc['text'], doc['doc_id'])
        embeddings.append(emb)
        valid_docs.append(doc)

    # 4. Build & Save Index
    search_engine = SearchEngine()
    search_engine.build_index(valid_docs, embeddings)
    
    # Pickle the search engine to reuse in API
    with open("search_engine_store.pkl", "wb") as f:
        pickle.dump(search_engine, f)
        
    print("Indexing Complete! Engine saved.")

if __name__ == "__main__":
    prepare_data()