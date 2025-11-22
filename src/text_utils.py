import re
import hashlib

def clean_text(text: str) -> str:
    # Lowercase
    text = text.lower()
    # Remove HTML tags (simple regex)
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()