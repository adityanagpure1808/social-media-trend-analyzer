



import sqlite3
import json
import traceback
from datetime import datetime
from services.vector_db import get_vector_collection
from services.tavily_client import get_platform_trends
from services.embedding_service import store_report_embeddings

DB_PATH = "database.db"


# =========================
# SOURCE URL EXTRACTOR
# =========================
def extract_source_url(item: dict) -> str | None:
    return (
        item.get("url")
        or item.get("link")
        or item.get("source")
        or item.get("href")
    )


# =========================
# PLATFORM NORMALIZATION
# =========================
def normalize_platform(platform: str | None) -> str:
    return platform.strip().lower() if platform else "general"


# =========================
# PLATFORM BACKGROUND
# =========================
def get_platform_background(platform: str) -> str:
    p = platform.lower()

    if p == "facebook":
        return "Facebook trends are driven by community discussions and viral sharing."
    if p == "linkedin":
        return "LinkedIn trends focus on professional conversations and industry insights."
    if p == "instagram":
        return "Instagram trends are shaped by visual storytelling and creators."

    return f"Trends on {platform.capitalize()} are influenced by community discussions."


# =========================
# HASHTAG GENERATOR
# =========================
def generate_hashtags(title: str) -> list[str]:
    if not title:
        return []

    words = title.lower().replace("-", " ").split()
    return [f"#{w}" for w in words if len(w) > 3][:5]


# =========================
# NORMALIZE TAVILY RESPONSE
# =========================
def normalize_tavily_report(tavily_results: list, platform: str) -> dict:
    return {
        "title": "Trend Report",
        "summary": "This report highlights trending topics and conversations.",
        "platform_background": get_platform_background(platform),
        "topics": [
            {
                "name": item.get("title", "Unknown Topic"),
                "description": (
                    item.get("content", "").strip()
                    if item.get("content")
                    else "No description available."
                ),
                "source_url": extract_source_url(item),
                "hashtags": generate_hashtags(item.get("title", "")),
                "popularity": min(len(item.get("content", "")) // 20, 100),
            }
            for item in tavily_results[:5]
        ],
    }


# =========================
# BACKGROUND REPORT JOB
# =========================
def generate_report(
    report_id: str,
    platform: str,
    query: str | None = None
) -> None:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    try:
        # STEP 1 — MARK RUNNING
        cursor.execute(
            """
            UPDATE reports
            SET status=?, progress=?, updated_at=?
            WHERE id=?
            """,
            ("running", 10, datetime.utcnow().isoformat(), report_id),
        )
        conn.commit()

        platform = normalize_platform(platform)

        # STEP 2 — BUILD SEARCH QUERY
        query_text: str = query.strip() if query else ""
        search_query = (
            f"trending topics on {platform} social media"
            if not query_text
            else f"{query_text} trending on {platform}"
        )

        # STEP 3 — CALL TAVILY
        tavily = get_platform_trends(search_query)

        if not tavily.get("success"):
            raise RuntimeError(tavily.get("error", "Tavily API failed"))

        # STEP 4 — NORMALIZE DATA
        normalized = normalize_tavily_report(
            tavily_results=tavily["data"],
            platform=platform,
        )

        # STEP 5 — SAVE REPORT
        cursor.execute(
            """
            UPDATE reports
            SET
                status=?,
                progress=?,
                title=?,
                summary=?,
                trending_topics=?,
                raw_report=?,
                updated_at=?
            WHERE id=?
            """,
            (
                "completed",
                100,
                normalized["title"],
                normalized["summary"],
                json.dumps({
                    "platform_background": normalized["platform_background"],
                    "topics": normalized["topics"],
                }),
                json.dumps(tavily["data"]),
                datetime.utcnow().isoformat(),
                report_id,
            ),
        )
        conn.commit()

        # STEP 6 — EMBEDDINGS (NON-FATAL)
        try:
            print("🧠 Attempting embeddings for:", report_id)

            # 🔥 CRITICAL FIX — PLATFORM INCLUDED IN KNOWLEDGE
            full_text = (
                f"Platform: {platform}\n\n"
                + normalized["platform_background"]
                + "\n\n"
                + normalized["summary"]
                + "\n\n"
                + "\n".join(
                    f"{t['name']}: {t['description']}"
                    for t in normalized["topics"]
                )
            )

            store_report_embeddings(
                report_id=report_id,
                content=full_text,
                metadata={
                    "platform": platform,
                    "title": normalized["title"],
                },
            )

            print("🧠 Embeddings completed for:", report_id)

        except RuntimeError as embed_error:
            # NON-FATAL — REPORT STILL VALID
            print("⚠️ Embeddings skipped (report still valid):", embed_error)

    except Exception as e:
        traceback.print_exc()

        cursor.execute(
            """
            UPDATE reports
            SET status=?, progress=?, error_message=?, updated_at=?
            WHERE id=?
            """,
            (
                "failed",
                0,
                str(e),
                datetime.utcnow().isoformat(),
                report_id,
            ),
        )
        conn.commit()

    finally:
        conn.close()


# =========================
# DEBUG VECTOR DB
# =========================
def debug_vector_dump():
    collection = get_vector_collection()
    print("🧠 TOTAL VECTORS IN DB:", collection.count())

    results = collection.get(limit=3)
    print("🔎 SAMPLE METADATA:", results.get("metadatas"))
