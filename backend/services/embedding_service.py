




# import os
# from chromadb import Client as ChromaClient
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer

# # =============================
# # LOCAL EMBEDDING MODEL
# # =============================
# # Runs fully offline — no API, no keys, no billing, no 404
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # =============================
# # CHROMA VECTOR DB
# # =============================
# chroma = ChromaClient(Settings(persist_directory="./chroma", anonymized_telemetry=False))
# collection = chroma.get_or_create_collection("reports")


# # =============================
# # TEXT CHUNKING
# # =============================
# def chunk_text(text: str, size: int = 800, overlap: int = 120):
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + size
#         chunk = text[start:end].strip()

#         if chunk:
#             chunks.append(chunk)

#         start = end - overlap

#     return chunks


# # =============================
# # STORE REPORT EMBEDDINGS
# # =============================
# def store_report_embeddings(report_id: str, content: str, metadata: dict):
#     print("🚨 ABOUT TO STORE EMBEDDINGS FOR:", report_id)

#     chunks = chunk_text(content)
#     print("🧩 Chunks:", len(chunks))

#     if not chunks:
#         raise RuntimeError("No chunks generated — cannot embed")

#     success_count = 0

#     for i, chunk in enumerate(chunks):
#         try:
#             # LOCAL EMBEDDING
#             embedding = model.encode(chunk).tolist()

#             collection.add(
#                 documents=[chunk],
#                 embeddings=[embedding],
#                 metadatas=[{
#                     **metadata,
#                     "report_id": report_id,
#                     "chunk_index": i
#                 }],
#                 ids=[f"{report_id}_{i}"]
#             )

#             success_count += 1

#         except Exception as e:
#             print("❌ EMBEDDINGS FAILED AT CHUNK", i, ":", e)
#             raise RuntimeError(f"Embedding failed at chunk {i}") from e

#     print(f"🧠 EMBEDDINGS SUCCESS — stored {success_count}/{len(chunks)} chunks")


# # =============================
# # SEMANTIC SEARCH
# # =============================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     try:
#         # LOCAL QUERY EMBEDDING
#         query_embedding = model.encode(query).tolist()

#     except Exception as e:
#         print("❌ Query embedding failed:", e)
#         return {"documents": [], "metadatas": []}

#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=k
#     )

#     docs = []
#     metas = []

#     if results.get("documents"):
#         for d, m in zip(results["documents"][0], results["metadatas"][0]):
#             if m.get("report_id") == report_id:
#                 docs.append(d)
#                 metas.append(m)

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(docs))

#     return {
#         "documents": docs,
#         "metadatas": metas
#     }


# # =============================
# # VECTOR HEALTH DEBUG
# # ====================
# def vector_health():
#     return {
#         "vector_count": collection.count(),
#         "provider": "local_sentence_transformers"
#     }





# import os
# from pathlib import Path
# from typing import Optional
# from chromadb import Client as ChromaClient
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer

# # =====================================================
# # PERSISTENT VECTOR STORAGE (Render disk)
# # =====================================================
# DATA_DIR = os.getenv("RENDER_DISK_PATH", "/data")
# VECTOR_DIR = os.path.join(DATA_DIR, "chroma")
# Path(VECTOR_DIR).mkdir(parents=True, exist_ok=True)


# # =====================================================
# # SINGLETONS (prevents multi-load crash)
# # =====================================================
# _model: Optional[SentenceTransformer] = None
# _collection = None


# # =====================================================
# # SAFE MODEL LOADER
# # =====================================================
# def get_model():
#     global _model
#     if _model is None:
#         print("🧠 Loading embedding model (first time only)...")
#         _model = SentenceTransformer("all-MiniLM-L6-v2")
#     return _model


# # =====================================================
# # VECTOR DB SINGLETON
# # =====================================================
# def get_collection():
#     global _collection
#     if _collection is None:
#         client = ChromaClient(Settings(
#             persist_directory=VECTOR_DIR,
#             anonymized_telemetry=False
#         ))
#         _collection = client.get_or_create_collection("reports")
#     return _collection


# # =====================================================
# # TEXT CHUNKING
# # =====================================================
# def chunk_text(text: str, size: int = 800, overlap: int = 120):
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + size
#         chunk = text[start:end].strip()
#         if chunk:
#             chunks.append(chunk)
#         start = end - overlap

#     return chunks


# # =====================================================
# # STORE EMBEDDINGS
# # =====================================================
# def store_report_embeddings(report_id: str, content: str, metadata: dict):
#     model = get_model()
#     collection = get_collection()

#     chunks = chunk_text(content)

#     if not chunks:
#         raise RuntimeError("No chunks generated")

#     for i, chunk in enumerate(chunks):
#         embedding = model.encode(chunk).tolist()

#         collection.add(
#             documents=[chunk],
#             embeddings=[embedding],
#             metadatas=[{
#                 **metadata,
#                 "report_id": report_id,
#                 "chunk_index": i
#             }],
#             ids=[f"{report_id}_{i}"]
#         )


# # =====================================================
# # SAFE SEMANTIC SEARCH
# # =====================================================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     try:
#         model = get_model()
#         collection = get_collection()

#         query_embedding = model.encode(query).tolist()

#         results = collection.query(
#             query_embeddings=[query_embedding],
#             n_results=k
#         )

#         docs = []
#         metas = []

#         if results.get("documents"):
#             for d, m in zip(results["documents"][0], results["metadatas"][0]):
#                 if m.get("report_id") == report_id:
#                     docs.append(d)
#                     metas.append(m)

#         return {"documents": docs, "metadatas": metas}

#     except Exception as e:
#         print("⚠️ semantic_search fallback:", e)
#         return {"documents": [], "metadatas": []}


# # =====================================================
# # HEALTH CHECK
# # =====================================================
# def vector_health():
#     try:
#         collection = get_collection()
#         return {"vector_count": collection.count(), "status": "ok"}
#     except Exception:
#         return {"vector_count": 0, "status": "error"}














from chromadb import Client as ChromaClient
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# =====================================================
# IN-MEMORY VECTOR DB (Render free tier safe)
# =====================================================
_client = None
_collection = None

# Default lightweight ONNX embedding model (~50MB)
embedding_function = embedding_functions.DefaultEmbeddingFunction()


# =====================================================
# VECTOR DB SINGLETON
# =====================================================
def get_collection():
    global _client, _collection

    if _collection is None:
        _client = ChromaClient(Settings(anonymized_telemetry=False))
        _collection = _client.get_or_create_collection(
            name="reports",
            embedding_function=embedding_function
        )

    return _collection


# =====================================================
# TEXT CHUNKING
# =====================================================
def chunk_text(text: str, size: int = 800, overlap: int = 120):
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


# =====================================================
# STORE EMBEDDINGS
# =====================================================
def store_report_embeddings(report_id: str, content: str, metadata: dict):
    collection = get_collection()
    chunks = chunk_text(content)

    if not chunks:
        return

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            metadatas=[{
                **metadata,
                "report_id": report_id,
                "chunk_index": i
            }],
            ids=[f"{report_id}_{i}"]
        )


# =====================================================
# SEMANTIC SEARCH
# =====================================================
def semantic_search(query: str, report_id: str, k: int = 5):
    try:
        collection = get_collection()

        results = collection.query(
            query_texts=[query],
            n_results=k
        )

        docs = []
        metas = []

        if results.get("documents"):
            for d, m in zip(results["documents"][0], results["metadatas"][0]):
                if m.get("report_id") == report_id:
                    docs.append(d)
                    metas.append(m)

        return {"documents": docs, "metadatas": metas}

    except Exception as e:
        print("semantic search failed:", e)
        return {"documents": [], "metadatas": []}


# =====================================================
# HEALTH
# =====================================================
def vector_health():
    try:
        collection = get_collection()
        return {"vector_count": collection.count(), "status": "ok"}
    except Exception:
        return {"vector_count": 0, "status": "error"}
