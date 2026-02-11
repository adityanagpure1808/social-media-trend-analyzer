


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
##above one i9s working






# import os

# VECTOR_DIR = "vector_store"
# COLLECTION_NAME = "reports"


# def get_vector_collection():
#     """
#     Lazy-load Chroma only when actually needed
#     Prevents Render OOM at startup
#     """
#     import chromadb
#     from chromadb.config import Settings

#     os.makedirs(VECTOR_DIR, exist_ok=True)

#     client = chromadb.Client(
#         Settings(
#             persist_directory=VECTOR_DIR,
#             anonymized_telemetry=False,
#         )
#     )

#     return client.get_or_create_collection(name=COLLECTION_NAME)







# vectordb.py
# Bridge file → keeps compatibility with old imports

from services.embedding_service import collection

def get_vector_collection():
    """
    Return SAME collection used by embedding_service
    Prevents dual database issue
    """
    return collection
