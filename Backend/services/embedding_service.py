




# def store_report_embeddings(
#     report_id: str,
#     content: str,
#     metadata: dict,
# ):
#     """
#     Stores CHUNKED embeddings for ONE report.
#     MUST persist for RAG to work.
#     """

#     collection = get_vector_collection()
#     embeddings_model = get_embedding_model()

#     chunks = chunk_text(content)
#     print("🧩 Chunks:", len(chunks))

#     if not chunks:
#         raise ValueError("No chunks generated")

#     vectors = embeddings_model.embed_documents(chunks)

#     collection.add(
#         documents=chunks,
#         embeddings=vectors,
#         metadatas=[
#             {
#                 **metadata,
#                 "report_id": report_id,
#                 "chunk_index": i,
#             }
#             for i in range(len(chunks))
#         ],
#         ids=[f"{report_id}_{i}" for i in range(len(chunks))],
#     )

#     print("🧠 Embeddings stored for report:", report_id)

#     # 🔥 THIS LINE WAS MISSING
#     persist()
#     print("💾 Vector store persisted to disk")








# # =========================
# # SEMANTIC SEARCH
# # =========================

# def semantic_search(
#     query: str,
#     report_id: Optional[str] = None,
#     top_k: int = 5,
# ):
#     collection = get_vector_collection()
#     embeddings_model = get_embedding_model()

#     query_embedding = embeddings_model.embed_query(query)

#     where = {"report_id": report_id} if report_id else None

#     result = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k,
#         where=where,
#     )

#     docs = result.get("documents", [[]])[0]
#     metas = result.get("metadatas", [[]])[0]

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(docs))
#     print("🏷 sample metadatas:", metas[:2])

#     return {
#         "documents": docs,
#         "metadatas": metas,
#     }

# # =========================
# # VECTOR HEALTH
# # =========================

# def vector_health():
#     collection = get_vector_collection()
#     return {
#         "vector_count": collection.count(),
#         "provider": "gemini",
#     }




# import os
# from typing import Optional

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from services.vector_db import get_vector_collection

# # =========================
# # EMBEDDING MODEL (GEMINI)
# # =========================

# def get_embedding_model():
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise RuntimeError("GEMINI_API_KEY not set")

#     return GoogleGenerativeAIEmbeddings(
#         # model="models/text-embedding-004",
#         model="models/embedding-001",

#         google_api_key=api_key,
#     )

# # =========================
# # CHUNKING
# # =========================

# def chunk_text(
#     text: str,
#     chunk_size: int = 500,
#     overlap: int = 50,
# ) -> list[str]:
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + chunk_size
#         chunk = text[start:end]

#         if chunk.strip():
#             chunks.append(chunk)

#         start = end - overlap

#     return chunks

# # =========================
# # STORE REPORT EMBEDDINGS
# # =========================

# def store_report_embeddings(
#     report_id: str,
#     content: str,
#     metadata: dict,
# ):
#     """
#     Stores CHUNKED embeddings for ONE report.
#     Chroma auto-persists — DO NOT call persist().
#     """

#     collection = get_vector_collection()
#     embeddings_model = get_embedding_model()

#     chunks = chunk_text(content)
#     print("🧩 Chunks:", len(chunks))

#     if not chunks:
#         raise ValueError("No chunks generated")

#     vectors = embeddings_model.embed_documents(chunks)

#     collection.add(
#         documents=chunks,
#         embeddings=vectors,
#         metadatas=[
#             {
#                 **metadata,
#                 "report_id": report_id,
#                 "chunk_index": i,
#             }
#             for i in range(len(chunks))
#         ],
#         ids=[f"{report_id}_{i}" for i in range(len(chunks))],
#     )

#     # ✅ FINAL LINE — NOTHING ELSE
#     print("🧠 Embeddings stored for report:", report_id)

# # =========================
# # SEMANTIC SEARCH
# # =========================

# def semantic_search(
#     query: str,
#     report_id: Optional[str] = None,
#     top_k: int = 5,
# ):
#     collection = get_vector_collection()
#     embeddings_model = get_embedding_model()

#     query_embedding = embeddings_model.embed_query(query)

#     where = {"report_id": {"$eq": report_id}} if report_id else None

#     result = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k,
#         where=where,
#     )

#     docs = result.get("documents", [[]])[0]
#     metas = result.get("metadatas", [[]])[0]

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(docs))
#     print("🏷 sample metadatas:", metas[:2])

#     return {
#         "documents": docs,
#         "metadatas": metas,
#     }


# # def semantic_search(
# #     query: str,
# #     report_id: Optional[str] = None,
# #     top_k: int = 5,
# # ):
# #     collection = get_vector_collection()
# #     embeddings_model = get_embedding_model()

# #     query_embedding = embeddings_model.embed_query(query)

# #     where = {"report_id": report_id} if report_id else None

# #     result = collection.query(
# #         query_embeddings=[query_embedding],
# #         n_results=top_k,
# #         where=where,
# #     )

# #     docs = result.get("documents", [[]])[0]
# #     metas = result.get("metadatas", [[]])[0]

# #     return {
# #         "documents": docs,
# #         "metadatas": metas,
# #     }

# # =========================
# # VECTOR HEALTH
# # =========================

# def vector_health():
#     collection = get_vector_collection()
#     return {
#         "vector_count": collection.count(),
#         "provider": "gemini",
#     }





# import os
# from google import genai
# from chromadb import Client
# from chromadb.config import Settings
# from google.genai import types

# # =============================
# # Gemini client
# # =============================
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# # =============================
# # Chroma DB
# # =============================
# chroma = Client(Settings(persist_directory="./chroma", anonymized_telemetry=False))
# collection = chroma.get_or_create_collection("reports")


# # =============================
# # STORE EMBEDDINGS
# # =============================
# def store_report_embeddings(report_id: str, content: str, metadata: dict):
#     print("🚨 ABOUT TO STORE EMBEDDINGS FOR:", report_id)

#     chunks = [content[i:i+800] for i in range(0, len(content), 800)]
#     print("🧩 Chunks:", len(chunks))

#     for i, chunk in enumerate(chunks):
#         try:
#             # response = client.models.embed_content(
#             #     # model="text-embedding-004",
#             #     # model="embedding-001",
#             #     model="gemini-2.0-flash",
#             #     contents=chunk
#             # )

#             response = client.models.embed_content(
#                 # model="text-embedding-3-large",
#                 model="embedding-001",
#                 contents=chunk
#             )


#             # embedding = response.embeddings[0].values
#             embedding = response.embeddings[0].embedding


#             collection.add(
#                 documents=[chunk],
#                 embeddings=[embedding],
#                 metadatas=[{**metadata, "report_id": report_id, "chunk_index": i}],
#                 ids=[f"{report_id}_{i}"]
#             )

#         except Exception as e:
#             print("❌ EMBEDDINGS FAILED:", e)
#             return

#     print("🧠 Embeddings stored for report:", report_id)


# # =============================
# # SEMANTIC SEARCH
# # =============================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     # response = client.models.embed_content(
#     #     # model="text-embedding-004",
#     #     # model="embedding-001",
#     #     model="gemini-2.0-flash",
#     #     contents=query
#     # )
    

#     response = client.models.embed_content(
#     # model="text-embedding-3-large",
#     model="embedding-001",
#     contents=query
#     )


#     # query_embedding = response.embeddings[0].values
#     embedding = response.embeddings[0].embedding


#     results = collection.query(
#         query_embeddings=[embedding],
#         n_results=k
#     )

#     docs = []
#     metas = []

#     for d, m in zip(results["documents"][0], results["metadatas"][0]):
#         if m.get("report_id") == report_id:
#             docs.append(d)
#             metas.append(m)

#     print("🔍 semantic_search report_id:", report_id)
#     print("📄 documents found:", len(docs))

#     return {"documents": docs, "metadatas": metas}




# # import os
# # # from google import genai
# # from chromadb import Client
# # from chromadb.config import Settings
# # # from google import genai
# # # from google.genai import types
# # from google.genai import Client
# from chromadb import Client as ChromaClient
# from chromadb.config import Settings
# from google.genai import Client as GeminiClient
# import os

# # client = Client(api_key=os.getenv("GOOGLE_API_KEY"))

# # # =============================
# # # Gemini Client (CORRECT API)
# # # =============================
# # # client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# # # =============================
# # # Chroma DB (persistent)
# # # =============================
# # chroma = Client(Settings(persist_directory="./chroma", anonymized_telemetry=False))
# # collection = chroma.get_or_create_collection("reports")




# # Gemini client (embeddings)
# gemini = GeminiClient(api_key=os.getenv("GOOGLE_API_KEY"))

# # Chroma vector DB
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
#         print("❌ No chunks generated")
#         return

#     for i, chunk in enumerate(chunks):
#         try:
#             # 🔥 CORRECT ENDPOINT (this fixes everything)
#             # response = gemini.embeddings.create(               # model="embedding-001",
#             response = gemini.models.embed_content(
#                 # input=chunk
#                 model="embedding-001",
#                 input=[chunk]
#                 )
            

#             embedding = response.data[0].embedding

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

#         except Exception as e:
#             print("❌ EMBEDDINGS FAILED:", e)
#             return

#     print("🧠 Embeddings stored for report:", report_id)


# # =============================
# # SEMANTIC SEARCH
# # =============================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     try:
#         # 🔥 SAME FIX HERE
#         # response = gemini.embeddings.create(
#         response = gemini.models.embed_content(
#             # model="embedding-001",
#             # input=query
#             model="embedding-001",
#             input=[query]
#         )

#         query_embedding = response.data[0].embedding

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
# # =============================
# def vector_health():
#     return {
#         "vector_count": collection.count(),
#         "provider": "google_genai_embeddings"
#     }






# import os
# from urllib import response
# from chromadb import Client as ChromaClient
# from chromadb.config import Settings

# from google import genai
# from google.genai import types

# gemini = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     http_options=types.HttpOptions(api_version="v1")
# )

# # from google.genai import Client as GeminiClient


# # # =============================
# # # CLIENTS
# # # =============================

# # # Gemini (Embeddings)
# # gemini = GeminiClient(api_key=os.getenv("GOOGLE_API_KEY"))

# # Chroma (Persistent Vector DB)
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
#         print("❌ No chunks generated")
#         return

#     for i, chunk in enumerate(chunks):
#         try:
#             # 🔥 CORRECT GOOGLE-GENAI EMBEDDING CALL
#             # response = gemini.models.embed_content(
#             #     # model="models/embedding-001",
#             #     model="models/text-embedding-004",

#             #     contents=chunk
#             # )


#             # response = gemini.models.embed_content(
#             #     model="text-embedding-004",
#             #     contents=chunk
#             # )

#             # embedding = response.embeddings[0].values


#             # embedding = response.embeddings[0].values


#             response = gemini.models.embed_text(
#                 model="text-embedding-004",
#                 texts=[chunk]
#             )
#             embedding = response.embeddings[0].values


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

#         except Exception as e:
#             print("❌ EMBEDDINGS FAILED:", e)
#             return

#     print("🧠 Embeddings stored for report:", report_id)


# # =============================
# # SEMANTIC SEARCH
# # =============================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     try:
#         # 🔥 CORRECT QUERY EMBEDDING
#         # response = gemini.models.embed_content(
#         #     # model="models/embedding-001",
#         #     model="models/text-embedding-004",

#         #     contents=query
#         # )

#         # query_embedding = response.embeddings[0].values
#         # response = gemini.models.embed_content(
#         #     model="text-embedding-004",
#         #     contents=query
#         # )

#         # query_embedding = response.embeddings[0].values


#         response = gemini.models.embed_text(
#             model="text-embedding-004",
#             texts=[query]
#         )   
#         query_embedding = response.embeddings[0].values



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
# # =============================
# def vector_health():
#     return {
#         "vector_count": collection.count(),
#         "provider": "google_genai_embeddings"
#     }







# import os
# from chromadb import Client as ChromaClient
# from chromadb.config import Settings
# from google import genai
# from google.genai import types


# # =============================
# # CLIENTS
# # =============================

# # Gemini Client (FORCE v1 API)
# gemini = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     http_options=types.HttpOptions(api_version="v1")
# )

# # Chroma persistent DB
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
#         print("❌ No chunks generated")
#         return

#     for i, chunk in enumerate(chunks):
#         try:
#             # ✅ CORRECT GOOGLE GENAI EMBEDDING CALL
#             response = gemini.embeddings.create(
#                 model="text-embedding-004",
#                 input=chunk
#             )

#             embedding = response.data[0].embedding

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

#         except Exception as e:
#             print("❌ EMBEDDINGS FAILED:", e)
#             return

#     print("🧠 Embeddings stored for report:", report_id)


# # =============================
# # SEMANTIC SEARCH
# # =============================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     try:
#         # ✅ CORRECT QUERY EMBEDDING
#         response = gemini.embeddings.create(
#             model="text-embedding-004",
#             input=query
#         )

#         query_embedding = response.data[0].embedding

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
# # =============================
# def vector_health():
#     return {
#         "vector_count": collection.count(),
#         "provider": "google_genai_embeddings"
#     }





# import os
# from chromadb import Client as ChromaClient
# from chromadb.config import Settings
# from google import genai
# from google.genai import types
# from sentence_transformers import SentenceTransformer

# # Local embedding model (no API, no billing, no 404)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # Gemini Client (v1 API REQUIRED)
# gemini = genai.Client(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     http_options=types.HttpOptions(api_version="v1")
# )

# # Chroma persistent DB
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
# # INTERNAL EMBEDDING HELPER
# # =============================
# def _embed(text: str):
#     """Correct embedding call for google-genai 1.x"""

#     response = gemini.models.embed_content(
#         model="text-embedding-004",
#         contents=[
#             types.Content(
#                 role="user",
#                 parts=[types.Part(text=text)]
#             )
#         ]
#     )

#     return response.embeddings[0].values






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
#             embedding = _embed(chunk)   # your existing helper

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


# # # =============================
# # # STORE REPORT EMBEDDINGS
# # # =============================
# # def store_report_embeddings(report_id: str, content: str, metadata: dict):
# #     print("🚨 ABOUT TO STORE EMBEDDINGS FOR:", report_id)

# #     chunks = chunk_text(content)
# #     print("🧩 Chunks:", len(chunks))

# #     if not chunks:
# #         print("❌ No chunks generated")
# #         return

# #     for i, chunk in enumerate(chunks):
# #         try:
# #             embedding = _embed(chunk)

# #             collection.add(
# #                 documents=[chunk],
# #                 embeddings=[embedding],
# #                 metadatas=[{
# #                     **metadata,
# #                     "report_id": report_id,
# #                     "chunk_index": i
# #                 }],
# #                 ids=[f"{report_id}_{i}"]
# #             )

# #         except Exception as e:
# #             print("❌ EMBEDDINGS FAILED:", e)
# #             return

# #     print("🧠 Embeddings stored for report:", report_id)


# # =============================
# # SEMANTIC SEARCH
# # =============================
# def semantic_search(query: str, report_id: str, k: int = 5):
#     try:
#         query_embedding = _embed(query)

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
# # =============================
# def vector_health():
#     return {
#         "vector_count": collection.count(),
#         "provider": "google_genai_embeddings"
#     }








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