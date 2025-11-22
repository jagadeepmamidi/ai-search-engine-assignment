import sqlite3
import json
import time
from src.config import DB_PATH

class CacheManager:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS embeddings (
            doc_id TEXT PRIMARY KEY,
            doc_hash TEXT,
            embedding TEXT,
            updated_at REAL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def get_entry(self, doc_id):
        cursor = self.conn.execute("SELECT doc_hash, embedding FROM embeddings WHERE doc_id=?", (doc_id,))
        return cursor.fetchone()

    def save_entry(self, doc_id, doc_hash, embedding_list):
        # We store embedding as a JSON string
        embedding_json = json.dumps(embedding_list)
        query = """
        INSERT OR REPLACE INTO embeddings (doc_id, doc_hash, embedding, updated_at)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (doc_id, doc_hash, embedding_json, time.time()))
        self.conn.commit()

    def close(self):
        self.conn.close()