





# from fastapi import FastAPI, HTTPException, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from datetime import datetime
# import os
# import uuid
# import json

# from services.dashboard_service import get_dashboard_stats
# from database.db import get_db

# # routers
# from routes.chat import router as chat_router
# from routes.export import router as export_router


# # =====================================================
# # APP (lifespan safe for Render)
# # =====================================================
# app = FastAPI(title="Social Media Trend Analyzer API")


# # =====================================================
# # CORS (auto works for local + production)
# # =====================================================
# FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =====================================================
# # DATABASE INIT (safe)
# # =====================================================
# def init_db():
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.executescript("""
#     CREATE TABLE IF NOT EXISTS platform_selection (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id TEXT NOT NULL,
#         platform TEXT NOT NULL,
#         selected_at TEXT NOT NULL
#     );

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
#     );

#     CREATE TABLE IF NOT EXISTS report_chat (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id TEXT,
#         report_id TEXT NOT NULL,
#         question TEXT NOT NULL,
#         answer TEXT NOT NULL,
#         source TEXT,
#         created_at TEXT NOT NULL
#     );
#     """)

#     conn.commit()
#     conn.close()


# @app.on_event("startup")
# def startup():
#     init_db()


# # =====================================================
# # MODELS
# # =====================================================
# class PlatformSelect(BaseModel):
#     userId: str
#     platform: str

# class ReportRequest(BaseModel):
#     userId: str
#     platform: str
#     query: str | None = None


# # =====================================================
# # PLATFORM
# # =====================================================
# @app.post("/api/platform/select")
# def select_platform(data: PlatformSelect):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO platform_selection (user_id, platform, selected_at) VALUES (?, ?, ?)",
#         (data.userId, data.platform, datetime.utcnow().isoformat()),
#     )

#     conn.commit()
#     conn.close()

#     return {"message": "Platform saved"}


# @app.get("/api/platform/current/{user_id}")
# def get_current_platform(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT platform FROM platform_selection WHERE user_id=? ORDER BY id DESC LIMIT 1",
#         (user_id,),
#     )

#     row = cursor.fetchone()
#     conn.close()

#     return {"platform": row["platform"] if row else None}


# # =====================================================
# # BACKGROUND REPORT GENERATION (Render safe)
# # =====================================================
# def run_report_generation(report_id: str, platform: str, query: str | None):
#     from services.report_service import generate_report
#     generate_report(report_id, platform, query)


# @app.post("/api/report/generate")
# def generate_report_api(data: ReportRequest, background_tasks: BackgroundTasks):
#     report_id = str(uuid.uuid4())

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO reports (id, user_id, platform, status, progress, created_at, updated_at)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (
#         report_id,
#         data.userId,
#         data.platform,
#         "pending",
#         0,
#         datetime.utcnow().isoformat(),
#         datetime.utcnow().isoformat()
#     ))

#     conn.commit()
#     conn.close()

#     background_tasks.add_task(run_report_generation, report_id, data.platform, data.query)

#     return {"report_id": report_id, "status": "pending"}


# # =====================================================
# # EMBEDDINGS (lazy import prevents boot crash)
# # =====================================================
# @app.post("/api/reports/{report_id}/embed")
# def embed_report(report_id: str):
#     from services.embedding_service import store_report_embeddings

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT summary, trending_topics, platform, title FROM reports WHERE id=?",
#         (report_id,)
#     )
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     topics_data = json.loads(row["trending_topics"]) if row["trending_topics"] else {}
#     topics = topics_data.get("topics", [])

#     content = (row["summary"] or "") + "\n\n" + "\n".join(
#         f"{t['name']}: {t['description']}" for t in topics
#     )

#     store_report_embeddings(
#         report_id=report_id,
#         content=content,
#         metadata={"platform": row["platform"], "title": row["title"]},
#     )

#     return {"status": "embeddings_generated"}


# # =====================================================
# # DASHBOARD
# # =====================================================
# @app.get("/api/dashboard/{user_id}")
# def dashboard_stats(user_id: str):
#     return get_dashboard_stats(user_id)


# # =====================================================
# # HEALTH
# # =====================================================
# @app.get("/health")
# def health_check():
#     return {"status": "ok", "time": datetime.utcnow().isoformat()}


# # routers LAST
# app.include_router(chat_router)
# app.include_router(export_router)







# from fastapi import FastAPI, HTTPException, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from datetime import datetime
# import os
# import uuid
# import json

# from services.dashboard_service import get_dashboard_stats
# from database.db import get_db

# # routers
# from routes.chat import router as chat_router
# from routes.export import router as export_router


# # =====================================================
# # APP
# # =====================================================
# app = FastAPI(title="Social Media Trend Analyzer API")


# # =====================================================
# # CORS
# # =====================================================
# FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # =====================================================
# # DATABASE INIT (POSTGRES SAFE)
# # =====================================================
# def init_db():
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS platform_selection (
#         id SERIAL PRIMARY KEY,
#         user_id TEXT NOT NULL,
#         platform TEXT NOT NULL,
#         selected_at TIMESTAMP NOT NULL
#     );
#     """)

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
#         created_at TIMESTAMP,
#         updated_at TIMESTAMP
#     );
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS report_chat (
#         id SERIAL PRIMARY KEY,
#         user_id TEXT,
#         report_id TEXT NOT NULL,
#         question TEXT NOT NULL,
#         answer TEXT NOT NULL,
#         source TEXT,
#         created_at TIMESTAMP NOT NULL
#     );
#     """)

#     conn.commit()


# @app.on_event("startup")
# def startup():
#     init_db()


# # =====================================================
# # MODELS
# # =====================================================
# class PlatformSelect(BaseModel):
#     userId: str
#     platform: str

# class ReportRequest(BaseModel):
#     userId: str
#     platform: str
#     query: str | None = None


# # =====================================================
# # PLATFORM
# # =====================================================
# @app.post("/api/platform/select")
# def select_platform(data: PlatformSelect):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "INSERT INTO platform_selection (user_id, platform, selected_at) VALUES (%s, %s, %s)",
#         (data.userId, data.platform, datetime.utcnow()),
#     )

#     conn.commit()
#     return {"message": "Platform saved"}


# @app.get("/api/platform/current/{user_id}")
# def get_current_platform(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT platform FROM platform_selection WHERE user_id=%s ORDER BY id DESC LIMIT 1",
#         (user_id,),
#     )

#     row = cursor.fetchone()
#     return {"platform": row["platform"] if row else None}


# # =====================================================
# # BACKGROUND REPORT GENERATION
# # =====================================================
# def run_report_generation(report_id: str, platform: str, query: str | None):
#     from services.report_service import generate_report
#     generate_report(report_id, platform, query)


# @app.post("/api/report/generate")
# def generate_report_api(data: ReportRequest, background_tasks: BackgroundTasks):
#     report_id = str(uuid.uuid4())

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#         INSERT INTO reports (id, user_id, platform, status, progress, created_at, updated_at)
#         VALUES (%s, %s, %s, %s, %s, %s, %s)
#     """, (
#         report_id,
#         data.userId,
#         data.platform,
#         "pending",
#         0,
#         datetime.utcnow(),
#         datetime.utcnow()
#     ))

#     conn.commit()

#     background_tasks.add_task(run_report_generation, report_id, data.platform, data.query)

#     return {"report_id": report_id, "status": "pending"}


# # =====================================================
# # EMBEDDINGS
# # =====================================================
# @app.post("/api/reports/{report_id}/embed")
# def embed_report(report_id: str):
#     from services.embedding_service import store_report_embeddings

#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT summary, trending_topics, platform, title FROM reports WHERE id=%s",
#         (report_id,)
#     )
#     row = cursor.fetchone()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     topics_data = json.loads(row["trending_topics"]) if row["trending_topics"] else {}
#     topics = topics_data.get("topics", [])

#     content = (row["summary"] or "") + "\n\n" + "\n".join(
#         f"{t['name']}: {t['description']}" for t in topics
#     )

#     store_report_embeddings(
#         report_id=report_id,
#         content=content,
#         metadata={"platform": row["platform"], "title": row["title"]},
#     )

#     return {"status": "embeddings_generated"}


# # =====================================================
# # DASHBOARD
# # =====================================================
# @app.get("/api/dashboard/{user_id}")
# def dashboard_stats(user_id: str):
#     return get_dashboard_stats(user_id)


# # =====================================================
# # HEALTH
# # =====================================================
# @app.get("/health")
# def health_check():
#     return {"status": "ok", "time": datetime.utcnow().isoformat()}


# # routers LAST
# app.include_router(chat_router)
# app.include_router(export_router)





from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import uuid
import json

from services.dashboard_service import get_dashboard_stats
from database.db import get_db

# routers
from routes.chat import router as chat_router
from routes.export import router as export_router


# =====================================================
# APP
# =====================================================
app = FastAPI(title="Social Media Trend Analyzer API")


# =====================================================
# CORS
# =====================================================
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# DATABASE INIT (POSTGRES SAFE)
# =====================================================
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platform_selection (
        id SERIAL PRIMARY KEY,
        user_id TEXT NOT NULL,
        platform TEXT NOT NULL,
        selected_at TIMESTAMP NOT NULL
    );
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
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS report_chat (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        report_id TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        source TEXT,
        created_at TIMESTAMP NOT NULL
    );
    """)

    conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    init_db()


# =====================================================
# MODELS
# =====================================================
class PlatformSelect(BaseModel):
    userId: str
    platform: str


class ReportRequest(BaseModel):
    userId: str
    platform: str
    query: str | None = None


# =====================================================
# PLATFORM
# =====================================================
@app.post("/api/platform/select")
def select_platform(data: PlatformSelect):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO platform_selection (user_id, platform, selected_at) VALUES (%s, %s, %s)",
        (data.userId, data.platform, datetime.utcnow()),
    )

    conn.commit()
    conn.close()

    return {"message": "Platform saved"}


@app.get("/api/platform/current/{user_id}")
def get_current_platform(user_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT platform FROM platform_selection WHERE user_id=%s ORDER BY id DESC LIMIT 1",
        (user_id,),
    )

    row = cursor.fetchone()
    conn.close()

    return {"platform": row["platform"] if row else None}


# =====================================================
# BACKGROUND REPORT GENERATION
# =====================================================
def run_report_generation(report_id: str, platform: str, query: str | None):
    from services.report_service import generate_report
    generate_report(report_id, platform, query)


@app.post("/api/report/generate")
def generate_report_api(data: ReportRequest, background_tasks: BackgroundTasks):
    report_id = str(uuid.uuid4())

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (id, user_id, platform, status, progress, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        report_id,
        data.userId,
        data.platform,
        "pending",
        0,
        datetime.utcnow(),
        datetime.utcnow()
    ))

    conn.commit()
    conn.close()

    background_tasks.add_task(run_report_generation, report_id, data.platform, data.query)

    return {"report_id": report_id, "status": "pending"}


# =====================================================
# EMBEDDINGS
# =====================================================
@app.post("/api/reports/{report_id}/embed")
def embed_report(report_id: str):
    from services.embedding_service import store_report_embeddings

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT summary, trending_topics, platform, title FROM reports WHERE id=%s",
        (report_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found")

    topics_data = json.loads(row["trending_topics"]) if row["trending_topics"] else {}
    topics = topics_data.get("topics", [])

    content = (row["summary"] or "") + "\n\n" + "\n".join(
        f"{t['name']}: {t['description']}" for t in topics
    )

    store_report_embeddings(
        report_id=report_id,
        content=content,
        metadata={"platform": row["platform"], "title": row["title"]},
    )

    return {"status": "embeddings_generated"}


# =====================================================
# DASHBOARD
# =====================================================
@app.get("/api/dashboard/{user_id}")
def dashboard_stats(user_id: str):
    return get_dashboard_stats(user_id)


# =====================================================
# HEALTH
# =====================================================
@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


# routers LAST
app.include_router(chat_router)
app.include_router(export_router)
