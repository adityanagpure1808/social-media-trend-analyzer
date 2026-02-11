


# import chromadb
# from chromadb.config import Settings
# import os

# VECTOR_DIR = "vector_store"
# COLLECTION_NAME = "reports"


# def get_vector_collection():
#     """
#     ALWAYS returns a persisted Chroma collection from disk.
#     Safe across processes.
#     """
#     os.makedirs(VECTOR_DIR, exist_ok=True)

#     client = chromadb.Client(
#         Settings(
#             persist_directory=VECTOR_DIR,
#             anonymized_telemetry=False,
#         )
#     )

#     return client.get_or_create_collection(name=COLLECTION_NAME)




"""
Vector DB Access Layer

This file exists only to provide a shared import location.
Actual Chroma instance lives in embedding_service singleton.
"""

from services.embedding_service import get_collection


def get_vector_collection():
    """
    Returns the shared persistent collection.
    DO NOT create new Chroma clients here.
    """
    return get_collection()
