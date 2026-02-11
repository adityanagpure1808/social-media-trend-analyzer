






import os
from chromadb import Client as ChromaClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# =============================
# LOCAL EMBEDDING MODEL
# =============================
# Runs fully offline — no API, no keys, no billing, no 404
model = SentenceTransformer("all-MiniLM-L6-v2")

# =============================
# CHROMA VECTOR DB
# =============================
chroma = ChromaClient(Settings(persist_directory="./chroma", anonymized_telemetry=False))
collection = chroma.get_or_create_collection("reports")


# =============================
# TEXT CHUNKING
# =============================
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


# =============================
# STORE REPORT EMBEDDINGS
# =============================
def store_report_embeddings(report_id: str, content: str, metadata: dict):
    print("🚨 ABOUT TO STORE EMBEDDINGS FOR:", report_id)

    chunks = chunk_text(content)
    print("🧩 Chunks:", len(chunks))

    if not chunks:
        raise RuntimeError("No chunks generated — cannot embed")

    success_count = 0

    for i, chunk in enumerate(chunks):
        try:
            # LOCAL EMBEDDING
            embedding = model.encode(chunk).tolist()

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    **metadata,
                    "report_id": report_id,
                    "chunk_index": i
                }],
                ids=[f"{report_id}_{i}"]
            )

            success_count += 1

        except Exception as e:
            print("❌ EMBEDDINGS FAILED AT CHUNK", i, ":", e)
            raise RuntimeError(f"Embedding failed at chunk {i}") from e

    print(f"🧠 EMBEDDINGS SUCCESS — stored {success_count}/{len(chunks)} chunks")


# =============================
# SEMANTIC SEARCH
# =============================
def semantic_search(query: str, report_id: str, k: int = 5):
    try:
        # LOCAL QUERY EMBEDDING
        query_embedding = model.encode(query).tolist()

    except Exception as e:
        print("❌ Query embedding failed:", e)
        return {"documents": [], "metadatas": []}

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    docs = []
    metas = []

    if results.get("documents"):
        for d, m in zip(results["documents"][0], results["metadatas"][0]):
            if m.get("report_id") == report_id:
                docs.append(d)
                metas.append(m)

    print("🔍 semantic_search report_id:", report_id)
    print("📄 documents found:", len(docs))

    return {
        "documents": docs,
        "metadatas": metas
    }


# =============================
# VECTOR HEALTH DEBUG
# ====================
def vector_health():
    return {
        "vector_count": collection.count(),
        "provider": "local_sentence_transformers"
    }