# Multi-Document Embedding Search Engine with Caching

## Project Overview

This project is a lightweight, embedding-based search engine capable of indexing and retrieving text documents based on semantic similarity.

The system utilizes Sentence Transformers for embedding generation, FAISS for high-performance vector similarity search, and SQLite for local caching to optimize processing time.

## Key Features

- **Semantic Search:** Uses the `all-MiniLM-L6-v2` model to retrieve documents based on meaning rather than just keyword matching.
- **Intelligent Caching:** Implements a hash-based caching mechanism using SQLite. Embeddings are only regenerated if the source text changes, significantly reducing processing time on subsequent runs.
- **High-Performance Indexing:** Utilizes FAISS (Facebook AI Similarity Search) for sub-millisecond vector retrieval.
- **Search Explainability:** The API provides a scoring metric and a keyword overlap analysis to explain why specific documents were returned.
- **Modular Architecture:** The codebase is structured into distinct modules (Ingestion, Caching, Embedding, Searching, API) for maintainability and scalability.

## Project Structure

```
search_engine_assignment/
├── data/
│ ├── docs/ # Directory for storing processed text files
│ ├── cache.db # SQLite database for embedding cache
│ └── vector_index.bin # Serialized FAISS index (optional persistence)
├── src/
│ ├── api.py # FastAPI application entry point
│ ├── config.py # Centralized configuration and path management
│ ├── embedder.py # Logic for loading models and generating embeddings
│ ├── search_engine.py # Logic for FAISS indexing and retrieval
│ ├── cache_manager.py # Database interactions for caching
│ └── text_utils.py # Text cleaning and hashing utilities
├── main.py # ETL Pipeline: Downloads data, generates embeddings, builds index
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

## Setup and Installation

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Environment Setup

It is recommended to use a virtual environment.

Windows:
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

## Usage Instructions

### Step 1: Data Ingestion and Indexing

Run the main pipeline script. This will download the "20 Newsgroups" dataset, process the text, generate embeddings (checking the cache first), and build the FAISS index.

python main.py

Note: The first run may take a few minutes to download the model and process data. Subsequent runs will be near-instant due to the SQLite caching mechanism.

### Step 2: Start the API Server

Launch the FastAPI server using uvicorn.

uvicorn src.api:app --reload

### Step 3: Access the Search API

Open your web browser and navigate to the Swagger UI documentation:
http://127.0.0.1:8000/docs

## API Documentation

### Endpoint: POST /search

Performs a semantic search on the indexed documents.

**Request Body:**

{
"query": "**symptoms and treatment of kidney stones**",
"top_k": 3
}

**Response:**

```json
{
"doc_id": "doc_056",
"score": 0.5798,
"preview": "Isn't there a relatively new treatment for kidney stones involving\n   a non-invasive use of ultra-sound where the patient is lowered\n   into some sort...",
"explanation": {
"overlapped_keywords": [
"stones",
"and",
"kidney",
"treatment",
"of"
        ],
"overlap_ratio": 0.83
      }
    },
```

## Design Decisions

### 1. Caching Strategy (SQLite vs JSON)

SQLite was chosen over JSON or Pickle for caching. SQLite supports atomic transactions, handles larger datasets efficiently without loading the entire file into RAM, and is robust against corruption during program interruptions.

### 2. Vector Search (FAISS)

FAISS IndexFlatIP (Inner Product) was selected. Since the embeddings are normalized before indexing, the Inner Product is mathematically equivalent to Cosine Similarity, which is the standard metric for semantic textual similarity.

### 3. Modularity

The code follows the Single Responsibility Principle. The API layer is decoupled from the Search logic, and the Embedding generation is decoupled from the Caching logic. This allows for easy swapping of components (e.g., changing the vector database or the embedding model) without refactoring the entire application.
