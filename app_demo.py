import streamlit as st
import os
from sklearn.datasets import fetch_20newsgroups
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# --- Setup Page ---
st.set_page_config(page_title="AI Search Demo")
st.title("AI Doc Search (Live Demo)")
st.info("Note: This is a standalone demo. The data is being generated on the fly!")

# --- Cached Resource (Runs once) ---
@st.cache_resource
def load_search_engine():
    # 1. Load Data
    with st.spinner("Downloading 20 Newsgroups Dataset..."):
        categories = ['sci.space', 'sci.med', 'comp.graphics']
        dataset = fetch_20newsgroups(subset='train', categories=categories, 
                                     remove=('headers', 'footers', 'quotes'))
    
    docs = []
    for i, text in enumerate(dataset.data[:100]): # Limit to 100 for speed
        if len(text) > 50:
            docs.append({"doc_id": f"doc_{i:03d}", "text": text})
            
    # 2. Load Model
    with st.spinner("Loading AI Model..."):
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
    # 3. Generate Embeddings
    with st.spinner("Indexing Documents..."):
        embeddings = model.encode([d['text'] for d in docs])
        
    # 4. Build Index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    
    return model, index, docs

# --- App Logic ---
try:
    model, index, docs = load_search_engine()
    
    query = st.text_input("Enter Query:", placeholder="NASA space mission launching...")
    
    if st.button("Search") and query:
        # Embed Query
        q_emb = model.encode([query])
        faiss.normalize_L2(q_emb)
        
        # Search
        distances, indices = index.search(q_emb, k=3)
        
        st.success("Found results!")
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                result_text = docs[idx]['text']
                score = float(distances[0][i])
                
                with st.container():
                    st.subheader(f" {docs[idx]['doc_id']} (Score: {score:.4f})")
                    st.text(result_text[:300] + "...")
                    st.divider()
                    
except Exception as e:
    st.error(f"Error loading system: {e}")