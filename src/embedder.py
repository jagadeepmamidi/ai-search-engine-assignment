from sentence_transformers import SentenceTransformer
from src.cache_manager import CacheManager
from src.text_utils import clean_text, compute_hash
import json

class EmbeddingModel:
    def __init__(self):
        # Load model once
        print("Loading Model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache = CacheManager()

    def get_embedding(self, text: str, doc_id: str = None):
        """
        Generates embedding. Checks cache first if doc_id is provided.
        """
        cleaned_text = clean_text(text)
        
        if doc_id:
            current_hash = compute_hash(cleaned_text)
            cached_entry = self.cache.get_entry(doc_id)

            if cached_entry:
                stored_hash, stored_emb_json = cached_entry
                # HIT: Hash matches, return cached embedding
                if stored_hash == current_hash:
                    return json.loads(stored_emb_json)
                # MISS: Hash different, regenerate (implicit in code below)
            
            # Generate new embedding
            embedding = self.model.encode(cleaned_text).tolist()
            self.cache.save_entry(doc_id, current_hash, embedding)
            return embedding
        
        # No doc_id (e.g., user query), just encode
        return self.model.encode(cleaned_text).tolist()