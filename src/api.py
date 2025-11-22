from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from src.embedder import EmbeddingModel
from src.text_utils import clean_text

app = FastAPI(title="Vector Search Engine")

# Load resources on startup
try:
    with open("search_engine_store.pkl", "rb") as f:
        search_engine = pickle.load(f)
    embedder = EmbeddingModel() # Re-init embedder logic
except FileNotFoundError:
    print("Error: Index not found. Run main.py first.")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search")
async def search(request: SearchRequest):
    # 1. Embed Query
    query_emb = embedder.get_embedding(request.query)
    
    # 2. Search Index
    results = search_engine.search(query_emb, request.top_k)
    
    # 3. Format Response with Explanation
    response_data = []
    for res in results:
        explanation = search_engine.explain_result(request.query, res['text'])
        
        response_data.append({
            "doc_id": res['doc_id'],
            "score": round(res['score'], 4),
            "preview": res['text'][:150] + "...",
            "explanation": explanation
        })
        
    return {"results": response_data}