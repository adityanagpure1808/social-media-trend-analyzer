# from fastapi import APIRouter, HTTPException
# from fastapi.responses import FileResponse
# from services.export_service import build_markdown_report
# from main import get_db
# import json
# import tempfile
# import os

# router = APIRouter()

# @router.get("/api/reports/{report_id}/export")
# def export_report(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         raise HTTPException(status_code=404, detail="Report not found")

#     report = dict(row)

#     # Parse JSON fields
#     if report.get("trending_topics"):
#         topics_data = json.loads(report["trending_topics"])
#         report["platform_background"] = topics_data.get("platform_background", "")
#         report["trending_topics"] = topics_data.get("topics", [])
#     else:
#         report["trending_topics"] = []

#     if report.get("sentiment_analysis"):
#         report["sentiment_analysis"] = json.loads(report["sentiment_analysis"])
#     else:
#         report["sentiment_analysis"] = {}

#     markdown = build_markdown_report(report)

#     # create temp file
#     temp = tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8")
#     temp.write(markdown)
#     temp.close()

#     filename = f"report_{report_id}.md"

#     return FileResponse(
#         path=temp.name,
#         filename=filename,
#         media_type="text/markdown"
#     )








from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.export_service import build_markdown_report
from database.db import get_db
import json
import tempfile
import os

router = APIRouter()

@router.get("/api/reports/{report_id}/export")
def export_report(report_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Report not found")

    report = dict(row)

    # Parse JSON fields
    if report.get("trending_topics"):
        topics_data = json.loads(report["trending_topics"])
        report["platform_background"] = topics_data.get("platform_background", "")
        report["trending_topics"] = topics_data.get("topics", [])
    else:
        report["trending_topics"] = []

    if report.get("sentiment_analysis"):
        report["sentiment_analysis"] = json.loads(report["sentiment_analysis"])
    else:
        report["sentiment_analysis"] = {}

    markdown = build_markdown_report(report)

    # create temp file
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8")
    temp.write(markdown)
    temp.close()

    filename = f"report_{report_id}.md"

    return FileResponse(
        path=temp.name,
        filename=filename,
        media_type="text/markdown"
    )
