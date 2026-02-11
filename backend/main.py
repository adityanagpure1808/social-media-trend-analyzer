# """
# Backend - FastAPI Application

# Available Endpoints:
#     GET /                    - Welcome message
#     GET /health              - Health check endpoint
#     GET /api/random-quote    - Sample endpoint to connect Frontend and Backend (generates random quote using Gemini LLM)

# To run this server:
#     uvicorn main:app --reload

# The server will start at: http://localhost:8000
# API documentation will be available at: http://localhost:8000/docs

# Setup:
#     1. Install dependencies: pip install -r requirements.txt
#     2. Get your Google API key from: https://makersuite.google.com/app/apikey
#     3. Create a .env file in the Backend directory with: GOOGLE_API_KEY=your_api_key_here
#     4. Run the server: uvicorn main:app --reload
# """

# import os
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Google Generative AI
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     print("Warning: GOOGLE_API_KEY not found in environment variables.")
#     print("Please create a .env file with: GOOGLE_API_KEY=your_api_key_here")
#     genai_configured = False
# else:
#     genai.configure(api_key=api_key)
#     genai_configured = True

# app = FastAPI(title="Backend API", version="0.1.0")

# # Enable CORS (Cross-Origin Resource Sharing) to allow frontend to connect
# # This is necessary because the frontend runs on a different port than the backend
# # Without CORS, browsers will block requests from frontend to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port and common React port
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# @app.get("/")
# async def root():
#     return {"message": "Hello from AI Interviewer Backend!"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

# @app.get("/api/random-quote")
# async def get_random_quote():
#     """
#     Sample endpoint to connect Frontend and Backend.
#     This is a simple example endpoint that generates a random inspirational quote using Google's Gemini LLM.
#     Students can use this endpoint to practice connecting their React frontend to the FastAPI backend.
    
#     Returns:
#         JSON response with AI-generated random quote
#     """
#     if not genai_configured:
#         raise HTTPException(
#             status_code=500,
#             detail="Google API key not configured. Please set GOOGLE_API_KEY in your .env file."
#         )
    
#     try:
#         # Make a simple LLM call to generate a random quote
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         response = model.generate_content("Tell me a random inspirational quote")
        
#         return {
#             "success": True,
#             "message": "Random quote generated successfully",
#             "data": {
#                 "quote": response.text,
#             }
#         }
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error generating quote: {str(e)}"


#         )






# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import sqlite3
# from datetime import datetime
# import os
# import uuid
# import threading
# import json
# from services.report_service import generate_report 
# from services.embedding_service import store_report_embeddings




# # =========================
# # APP SETUP
# # =========================
# app = FastAPI(title="Social Media Trend Analyzer API")

# # =========================
# # CORS
# # =========================
# ALLOWED_ORIGINS = os.getenv(
#     "ALLOWED_ORIGINS",
#     "http://localhost:5173"
# ).split(",")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # DATABASE
# # =========================
# DB_PATH = os.getenv("DB_PATH", "database.db")

# def get_db():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.on_event("startup")
# def startup():
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS platform_selection (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id TEXT NOT NULL,
#         platform TEXT NOT NULL,
#         selected_at TEXT NOT NULL
#     )
#     """)

#     # DEV SAFE – reset schema
#     cursor.execute("DROP TABLE IF EXISTS reports")

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS reports (
#         id TEXT PRIMARY KEY,
#         user_id TEXT,
#         platform TEXT NOT NULL,
#         status TEXT NOT NULL,
#         progress INTEGER DEFAULT 0,

#         title TEXT,
#         summary TEXT,

#         trending_topics TEXT,
#         sentiment_analysis TEXT,
#         raw_report TEXT,

#         error_message TEXT,

#         created_at TEXT,
#         updated_at TEXT
#     )
#     """)

#     conn.commit()
#     conn.close()

# # =========================
# # MODELS
# # =========================
# class PlatformSelect(BaseModel):
#     userId: str
#     platform: str

# # 🔹 STEP 1 — UPDATED MODEL
# class ReportRequest(BaseModel):
#     userId: str
#     platform: str
#     query: str | None = None


# class EmbedRequest(BaseModel):
#     report_id: str


# class SearchRequest(BaseModel):
#     query: str


# # =========================
# # PLATFORM APIs
# # =========================
# @app.post("/api/platform/select")
# def select_platform(data: PlatformSelect):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO platform_selection (user_id, platform, selected_at)
#         VALUES (?, ?, ?)
#         """,
#         (data.userId, data.platform, datetime.utcnow().isoformat())
#     )

#     conn.commit()
#     conn.close()

#     return {"message": "Platform saved"}


# @app.get("/api/platform/current/{user_id}")
# def get_current_platform(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT platform
#         FROM platform_selection
#         WHERE user_id = ?
#         ORDER BY id DESC
#         LIMIT 1
#         """,
#         (user_id,)
#     )

#     row = cursor.fetchone()
#     conn.close()

#     return {"platform": row["platform"] if row else None}

# # =========================
# # STEP 5 — GENERATE REPORT
# # =========================
# @app.post("/api/report/generate")
# def generate_report_api(data: ReportRequest):
#     report_id = str(uuid.uuid4())

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO reports
#         (id, user_id, platform, status, progress, created_at, updated_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             report_id,
#             data.userId,
#             data.platform,
#             "pending",
#             0,
#             datetime.utcnow().isoformat(),
#             datetime.utcnow().isoformat()
#         )
#     )

#     conn.commit()
#     conn.close()

#     # 🔹 STEP 2 — PASS query TO BACKGROUND JOB
#     threading.Thread(
#         target=generate_report,
#         args=(report_id, data.platform, data.query),
#         daemon=True
#     ).start()

#     return {"report_id": report_id, "status": "pending"}


# # STEP 6 — STATUS (POLLING)
# @app.get("/api/reports/{report_id}/status")
# def report_status(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT status, progress FROM reports WHERE id=?",
#         (report_id,)
#     )

#     row = cursor.fetchone()
#     conn.close()

#     return dict(row) if row else {"status": "not_found"}

# # =========================
# # STEP 6.5 — GET ALL REPORTS FOR A USER (LIST VIEW)
# # =========================
# @app.get("/api/reports/user/{user_id}")
# def get_user_reports(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT
#             id,
#             platform,
#             title,
#             status,
#             created_at
#         FROM reports
#         WHERE user_id = ?
#         ORDER BY created_at DESC
#         """,
#         (user_id,)
#     )

#     rows = cursor.fetchall()
#     conn.close()

#     return [dict(row) for row in rows]





# # =========================
# # STEP 7 — FINAL REPORT
# # =========================
# @app.get("/api/reports/{report_id}")
# def get_report(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     report = dict(row)

#     if report["trending_topics"]:
#         topics_data = json.loads(report["trending_topics"])
#         report["platform_background"] = topics_data.get("platform_background", "")
#         report["trending_topics"] = topics_data.get("topics", [])
#     else:
#         report["platform_background"] = ""
#         report["trending_topics"] = []

#     if report["sentiment_analysis"]:
#         report["sentiment_analysis"] = json.loads(report["sentiment_analysis"])
#     else:
#         report["sentiment_analysis"] = {}

#     return report





# # =========================
# # STEP 8 — GENERATE EMBEDDINGS (ON DEMAND)
# # =========================
# @app.post("/api/reports/{report_id}/embed")
# def embed_report(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT
#             summary,
#             trending_topics,
#             platform,
#             title
#         FROM reports
#         WHERE id = ?
#         """,
#         (report_id,)
#     )

#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     topics_data = json.loads(row["trending_topics"]) if row["trending_topics"] else {}
#     topics = topics_data.get("topics", [])

#     content = (
#         (row["summary"] or "")
#         + "\n\n"
#         + "\n".join(
#             t["name"] + ": " + t["description"]
#             for t in topics
#         )
#     )

#     store_report_embeddings(
#         report_id=report_id,
#         content=content,
#         metadata={
#             "platform": row["platform"],
#             "title": row["title"],
#         }
#     )

#     return {"status": "embeddings_generated"}



# # =========================
# # STEP 9 — SEMANTIC SEARCH
# # =========================
# @app.post("/api/reports/search")
# def search_reports(data: SearchRequest):
#     from services.embedding_service import semantic_search

#     results = semantic_search(data.query)

#     return {
#         "documents": results.get("documents", []),
#         "metadata": results.get("metadatas", []),
#     }


# # =========================
# # HEALTH CHECK
# # =========================
# @app.get("/health")
# def health_check():
#     return {
#         "status": "ok",
#         "timestamp": datetime.utcnow().isoformat()
#     }

# @app.get("/api/reports/debug/vector-health")
# def debug_vector_health():
#     from services.embedding_service import vector_health
#     return vector_health()





# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import sqlite3
# from datetime import datetime
# import os
# import uuid
# import threading
# import json

# # from services.report_service import generate_report
# # from services.embedding_service import store_report_embeddings
# # from dotenv import load_dotenv
# # load_dotenv()

# # #added
# # # from routes import chat

# # # app.include_router(chat.router)
# # from fastapi import APIRouter
# # from models.chat import ChatRequest
# # from services.chat_service import save_chat_message, get_chat_history
# # from services.rag_service import answer_question_about_report
# # from routes.chat import router as chat_router

# from services.report_service import generate_report
# from services.embedding_service import store_report_embeddings

# from models.chat import ChatRequest
# from services.chat_service import save_chat_message, get_chat_history
# from services.rag_service import answer_question_about_report
# from routes.chat import router as chat_router
# from routes.export import router as export_router




# # =========================
# # APP SETUP
# # =========================
# app = FastAPI(title="Social Media Trend Analyzer API")

# #added
# # app.include_router(chat_router)

# # =========================
# # CORS
# # =========================
# ALLOWED_ORIGINS = os.getenv(
#     "ALLOWED_ORIGINS",
#     "http://localhost:5173,http://localhost:5174"
# ).split(",")
# # ALLOWED_ORIGINS = os.getenv(
# #     "ALLOWED_ORIGINS",
# #     "http://localhost:5173"
# # ).split(",")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=ALLOWED_ORIGINS,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ✅ ADD THIS HERE (ONLY HERE)
# app.include_router(chat_router)
# app.include_router(export_router) 

# # =========================
# # DATABASE
# # =========================
# DB_PATH = os.getenv("DB_PATH", "database.db")

# def get_db():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn

# @app.on_event("startup")
# def startup():
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS platform_selection (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id TEXT NOT NULL,
#         platform TEXT NOT NULL,
#         selected_at TEXT NOT NULL
#     )
#     """)

#     # ✅ PRODUCTION SAFE (NO DROP)
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS reports (
#         id TEXT PRIMARY KEY,
#         user_id TEXT,
#         platform TEXT NOT NULL,
#         status TEXT NOT NULL,
#         progress INTEGER DEFAULT 0,

#         title TEXT,
#         summary TEXT,

#         trending_topics TEXT,
#         sentiment_analysis TEXT,
#         raw_report TEXT,

#         error_message TEXT,

#         created_at TEXT,
#         updated_at TEXT
#     )
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS report_chat (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id TEXT,
#     report_id TEXT NOT NULL,
#     question TEXT NOT NULL,
#     answer TEXT NOT NULL,
#     source TEXT,
#     created_at TEXT NOT NULL
#     )
#     """)


#     # cursor.execute("""
#     # CREATE TABLE IF NOT EXISTS report_chat (
#     #     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     #     report_id TEXT NOT NULL,
#     #     question TEXT NOT NULL,
#     #     answer TEXT NOT NULL,
#     #     source TEXT,
#     #     created_at TEXT NOT NULL
#     # )
#     # """)
#     # cursor.execute("""
#     # CREATE TABLE IF NOT EXISTS report_chat (
#     # id INTEGER PRIMARY KEY AUTOINCREMENT,
#     # user_id TEXT,
#     # report_id TEXT NOT NULL,
#     # question TEXT NOT NULL,
#     # answer TEXT NOT NULL,
#     # source TEXT,
#     # created_at TEXT NOT NULL
#     # )
#     # """)



#     conn.commit()
#     conn.close()

# # =========================
# # MODELS
# # =========================
# class PlatformSelect(BaseModel):
#     userId: str
#     platform: str

# class ReportRequest(BaseModel):
#     userId: str
#     platform: str
#     query: str | None = None

# class SearchRequest(BaseModel):
#     query: str

# class RAGQueryRequest(BaseModel):
#     report_id: str
#     question: str




# # =========================
# # PLATFORM APIs
# # =========================
# @app.post("/api/platform/select")
# def select_platform(data: PlatformSelect):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO platform_selection (user_id, platform, selected_at)
#         VALUES (?, ?, ?)
#         """,
#         (data.userId, data.platform, datetime.utcnow().isoformat())
#     )

#     conn.commit()
#     conn.close()

#     return {"message": "Platform saved"}

# @app.get("/api/platform/current/{user_id}")
# def get_current_platform(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT platform
#         FROM platform_selection
#         WHERE user_id = ?
#         ORDER BY id DESC
#         LIMIT 1
#         """,
#         (user_id,)
#     )

#     row = cursor.fetchone()
#     conn.close()

#     return {"platform": row["platform"] if row else None}

# # =========================
# # GENERATE REPORT
# # =========================
# @app.post("/api/report/generate")
# def generate_report_api(data: ReportRequest):
#     report_id = str(uuid.uuid4())

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         INSERT INTO reports
#         (id, user_id, platform, status, progress, created_at, updated_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#         """,
#         (
#             report_id,
#             data.userId,
#             data.platform,
#             "pending",
#             0,
#             datetime.utcnow().isoformat(),
#             datetime.utcnow().isoformat()
#         )
#     )

#     conn.commit()
#     conn.close()

#     threading.Thread(
#         target=generate_report,
#         args=(report_id, data.platform, data.query),
#         daemon=True
#     ).start()

#     return {"report_id": report_id, "status": "pending"}

# # =========================
# # STATUS (POLLING) ✅ FIXED
# # =========================
# @app.get("/api/reports/{report_id}/status")
# def report_status(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT status, progress, error_message
#         FROM reports
#         WHERE id = ?
#         """,
#         (report_id,)
#     )

#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         return {"status": "not_found"}

#     return {
#         "status": row["status"],
#         "progress": row["progress"] or 0,
#         "error_message": row["error_message"],
#     }

# # =========================
# # LIST USER REPORTS
# # =========================
# @app.get("/api/reports/user/{user_id}")
# def get_user_reports(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT id, platform, title, status, created_at
#         FROM reports
#         WHERE user_id = ?
#         ORDER BY created_at DESC
#         """,
#         (user_id,)
#     )

#     rows = cursor.fetchall()
#     conn.close()

#     return [dict(row) for row in rows]

# # =========================
# # FINAL REPORT
# # =========================
# @app.get("/api/reports/{report_id}")
# def get_report(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     report = dict(row)

#     if report["trending_topics"]:
#         topics_data = json.loads(report["trending_topics"])
#         report["platform_background"] = topics_data.get("platform_background", "")
#         report["trending_topics"] = topics_data.get("topics", [])
#     else:
#         report["platform_background"] = ""
#         report["trending_topics"] = []

#     if report["sentiment_analysis"]:
#         report["sentiment_analysis"] = json.loads(report["sentiment_analysis"])
#     else:
#         report["sentiment_analysis"] = {}

#     return report

# # =========================
# # EMBEDDINGS (ON DEMAND)
# # =========================
# @app.post("/api/reports/{report_id}/embed")
# def embed_report(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         """
#         SELECT summary, trending_topics, platform, title
#         FROM reports
#         WHERE id = ?
#         """,
#         (report_id,)
#     )

#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     topics_data = json.loads(row["trending_topics"]) if row["trending_topics"] else {}
#     topics = topics_data.get("topics", [])

#     content = (
#         (row["summary"] or "")
#         + "\n\n"
#         + "\n".join(f"{t['name']}: {t['description']}" for t in topics)
#     )

#     store_report_embeddings(
#         report_id=report_id,
#         content=content,
#         metadata={
#             "platform": row["platform"],
#             "title": row["title"],
#         }
#     )

#     return {"status": "embeddings_generated"}

# # =========================
# # SEMANTIC SEARCH
# # =========================
# @app.post("/api/reports/search")
# def search_reports(data: SearchRequest):
#     # from services.embedding_service import semantic_search
#     from services.embedding_service import semantic_search


#     results = semantic_search(data.query)

#     return {
#         "documents": results.get("documents", []),
#         "metadata": results.get("metadatas", []),
#     }

# # =========================
# # DEBUG / HEALTH
# # =========================
# @app.get("/api/reports/debug/vector-health")
# def debug_vector_health():
#     # from services.embedding_service import vector_health
#     from services.embedding_service import vector_health

#     return vector_health()

# @app.get("/health")
# def health_check():
#     return {
#         "status": "ok",
#         "timestamp": datetime.utcnow().isoformat()
#     }



# # =========================
# # RAG — QUESTION ANSWERING
# # =========================
# @app.post("/api/reports/rag")
# def ask_report_question(data: RAGQueryRequest):
#     # from services.rag_service import answer_question_about_report
#     from services.rag_service import answer_question_about_report


#     answer = answer_question_about_report(
#         report_id=data.report_id,
#         question=data.question
#     )

#     return {
#         "answer": answer
#     }




# #added
# # router = APIRouter()

# # @router.post("/api/reports/chat")
# # def chat_with_report(payload: ChatRequest):
# #     answer = answer_question_about_report(
# #         report_id=payload.report_id,
# #         question=payload.question
# #     )

# #     save_chat_message(
# #         report_id=payload.report_id,
# #         question=payload.question,
# #         answer=answer,
# #         source="rag"
# #     )

# #     return {
# #         "answer": answer,
# #         "source": "rag"
# #     }


# # @router.get("/api/reports/{report_id}/chat")
# # def get_report_chat(report_id: str):
# #     return get_chat_history(report_id)





from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import uuid
import threading
import json
from services.dashboard_service import get_dashboard_stats



# Services
from services.report_service import generate_report
from services.embedding_service import store_report_embeddings

# Chat
from routes.chat import router as chat_router

# Export
from routes.export import router as export_router

# Shared DB (FIXED — NO CIRCULAR IMPORT)
from database.db import get_db


# =========================
# APP SETUP
# =========================
app = FastAPI(title="Social Media Trend Analyzer API")


# =========================
# CORS
# =========================
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:5174"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
# app.include_router(chat_router)
app.include_router(export_router)


# =========================
# STARTUP — CREATE TABLES
# =========================
@app.on_event("startup")
def startup():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platform_selection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        platform TEXT NOT NULL,
        selected_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        platform TEXT NOT NULL,
        status TEXT NOT NULL,
        progress INTEGER DEFAULT 0,
        title TEXT,
        summary TEXT,
        trending_topics TEXT,
        sentiment_analysis TEXT,
        raw_report TEXT,
        error_message TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS report_chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        report_id TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        source TEXT,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# =========================
# MODELS
# =========================
class PlatformSelect(BaseModel):
    userId: str
    platform: str

class ReportRequest(BaseModel):
    userId: str
    platform: str
    query: str | None = None

class SearchRequest(BaseModel):
    query: str

class RAGQueryRequest(BaseModel):
    report_id: str
    question: str


# =========================
# PLATFORM APIs
# =========================
@app.post("/api/platform/select")
def select_platform(data: PlatformSelect):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO platform_selection (user_id, platform, selected_at)
        VALUES (?, ?, ?)
        """,
        (data.userId, data.platform, datetime.utcnow().isoformat())
    )

    conn.commit()
    conn.close()

    return {"message": "Platform saved"}


@app.get("/api/platform/current/{user_id}")
def get_current_platform(user_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT platform
        FROM platform_selection
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return {"platform": row["platform"] if row else None}


# =========================
# GENERATE REPORT
# =========================
@app.post("/api/report/generate")
def generate_report_api(data: ReportRequest):
    report_id = str(uuid.uuid4())

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO reports
        (id, user_id, platform, status, progress, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            report_id,
            data.userId,
            data.platform,
            "pending",
            0,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    threading.Thread(
        target=generate_report,
        args=(report_id, data.platform, data.query),
        daemon=True
    ).start()

    return {"report_id": report_id, "status": "pending"}


# =========================
# REPORT STATUS
# =========================
@app.get("/api/reports/{report_id}/status")
def report_status(report_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status, progress, error_message FROM reports WHERE id=?",
        (report_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"status": "not_found"}

    return {
        "status": row["status"],
        "progress": row["progress"] or 0,
        "error_message": row["error_message"],
    }


# =========================
# FINAL REPORT
# =========================
@app.get("/api/reports/{report_id}")
def get_report(report_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found")

    report = dict(row)

    if report["trending_topics"]:
        topics_data = json.loads(report["trending_topics"])
        report["platform_background"] = topics_data.get("platform_background", "")
        report["trending_topics"] = topics_data.get("topics", [])
    else:
        report["platform_background"] = ""
        report["trending_topics"] = []

    if report["sentiment_analysis"]:
        report["sentiment_analysis"] = json.loads(report["sentiment_analysis"])
    else:
        report["sentiment_analysis"] = {}

    return report


# =========================
# EMBEDDINGS
# =========================
@app.post("/api/reports/{report_id}/embed")
def embed_report(report_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT summary, trending_topics, platform, title FROM reports WHERE id=?",
        (report_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found")

    topics_data = json.loads(row["trending_topics"]) if row["trending_topics"] else {}
    topics = topics_data.get("topics", [])

    content = (
        (row["summary"] or "")
        + "\n\n"
        + "\n".join(f"{t['name']}: {t['description']}" for t in topics)
    )

    store_report_embeddings(
        report_id=report_id,
        content=content,
        metadata={"platform": row["platform"], "title": row["title"]}
    )

    return {"status": "embeddings_generated"}


#dashboard stats

@app.get("/api/dashboard/{user_id}")
def dashboard_stats(user_id: str):
    return get_dashboard_stats(user_id)

# =========================
# USER REPORTS (DASHBOARD LIST)
# =========================
@app.get("/api/reports/user/{user_id}", tags=["Dashboard"])
def get_user_reports(user_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, platform, title, status, created_at
        FROM reports
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =========================
# HEALTH
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


#changed position
app.include_router(chat_router)