from fastapi import APIRouter
from database.db import get_db

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/user/{user_id}")
def get_user_reports(user_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, platform, status, progress, title, created_at
        FROM reports
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    reports = cursor.fetchall()
    conn.close()

    return reports




@router.get("/{report_id}/status")
def get_report_status(report_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, status, progress, title, summary, created_at, updated_at
        FROM reports
        WHERE id = %s
    """, (report_id,))

    report = cursor.fetchone()
    conn.close()

    if not report:
        return {"status": "not_found"}

    return report
