import faiss
import numpy as np
import pickle
import os
from src.config import INDEX_PATH

class SearchEngine:
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension) # Inner Product (Cosine if normalized)
        self.doc_map = [] # Maps FAISS ID to (doc_id, raw_text)
    
    def build_index(self, documents, embeddings):
        """
        documents: List of dicts {'doc_id': str, 'text': str}
        embeddings: List of lists (vectors)
        """
        print("Building FAISS Index...")
        vectors = np.array(embeddings).astype('float32')
        
        # Normalize vectors for Cosine Similarity via Inner Product
        faiss.normalize_L2(vectors)
        
        self.index.reset()
        self.index.add(vectors)
        
        # Store document data in memory (simple approach for <200 docs)
        self.doc_map = documents
        
        

    def search(self, query_vector, top_k=5):
        query_vec = np.array([query_vector]).astype('float32')
        faiss.normalize_L2(query_vec)
        
        distances, indices = self.index.search(query_vec, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1: continue 
            doc_data = self.doc_map[idx]
            score = float(distances[0][i])
            results.append({
                "doc_id": doc_data['doc_id'],
                "score": score,
                "text": doc_data['text']
            })
        return results

    def explain_result(self, query_text, result_text):
        """Simple keyword overlap explanation"""
        q_tokens = set(query_text.lower().split())
        d_tokens = set(result_text.lower().split())
        
        overlap = q_tokens.intersection(d_tokens)
        ratio = len(overlap) / len(q_tokens) if len(q_tokens) > 0 else 0
        
        return {
            "overlapped_keywords": list(overlap),
            "overlap_ratio": round(ratio, 2)
        }