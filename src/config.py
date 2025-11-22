import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCS_DIR = os.path.join(DATA_DIR, "docs")
DB_PATH = os.path.join(DATA_DIR, "cache.db")
INDEX_PATH = os.path.join(DATA_DIR, "vector_index.bin")

os.makedirs(DOCS_DIR, exist_ok=True)