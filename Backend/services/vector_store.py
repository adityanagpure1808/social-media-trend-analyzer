



from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

VECTOR_DB_PATH = "vector_store"

# singleton instance
_vector_store = None


def load_vector_store():
    """Initialize vector database (only once)"""
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    # IMPORTANT:
    # No embedding_function here
    # We generate embeddings manually in embedding_service.py
    _vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH
    )

    print("\n🔥 VECTOR STORE LOADED")
    print("📦 VECTOR COUNT:", _vector_store._collection.count())

    return _vector_store


def get_vector_store():
    """Safe accessor (works in background jobs too)"""
    global _vector_store

    if _vector_store is None:
        return load_vector_store()

    return _vector_store
