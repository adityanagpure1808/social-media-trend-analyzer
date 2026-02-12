# import sqlite3
# import os

# DB_PATH = os.getenv("DB_PATH", "database.db")


# def get_db():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


# def get_dashboard_stats(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     # total reports
#     cursor.execute("""
#         SELECT COUNT(*) as total_reports
#         FROM reports
#         WHERE user_id = ?
#     """, (user_id,))
#     total_reports = cursor.fetchone()["total_reports"]

#     # completed reports
#     cursor.execute("""
#         SELECT COUNT(*) as completed_reports
#         FROM reports
#         WHERE user_id = ? AND status = 'completed'
#     """, (user_id,))
#     completed_reports = cursor.fetchone()["completed_reports"]

#     # failed reports
#     cursor.execute("""
#         SELECT COUNT(*) as failed_reports
#         FROM reports
#         WHERE user_id = ? AND status = 'failed'
#     """, (user_id,))
#     failed_reports = cursor.fetchone()["failed_reports"]

#     # last selected platform
#     cursor.execute("""
#         SELECT platform
#         FROM platform_selection
#         WHERE user_id = ?
#         ORDER BY id DESC LIMIT 1
#     """, (user_id,))
#     row = cursor.fetchone()
#     platform = row["platform"] if row else None

#     conn.close()

#     return {
#         "total_reports": total_reports,
#         "completed_reports": completed_reports,
#         "failed_reports": failed_reports,
#         "current_platform": platform
#     }




# import sqlite3
# import os

# DB_PATH = os.getenv("DB_PATH", "database.db")


# def get_db():
#     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
#     conn.row_factory = sqlite3.Row
#     return conn


# def get_dashboard_stats(user_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     # total reports
#     cursor.execute("""
#         SELECT COUNT(*) as total_reports
#         FROM reports
#         WHERE user_id = ?
#     """, (user_id,))
#     total_reports = cursor.fetchone()["total_reports"]

#     # completed reports
#     cursor.execute("""
#         SELECT COUNT(*) as completed_reports
#         FROM reports
#         WHERE user_id = ? AND status = 'completed'
#     """, (user_id,))
#     completed_reports = cursor.fetchone()["completed_reports"]

#     # failed reports
#     cursor.execute("""
#         SELECT COUNT(*) as failed_reports
#         FROM reports
#         WHERE user_id = ? AND status = 'failed'
#     """, (user_id,))
#     failed_reports = cursor.fetchone()["failed_reports"]

#     # last selected platform
#     cursor.execute("""
#         SELECT platform
#         FROM platform_selection
#         WHERE user_id = ?
#         ORDER BY id DESC LIMIT 1
#     """, (user_id,))
#     row = cursor.fetchone()
#     platform = row["platform"] if row else None

#     conn.close()

#     return {
#         "total_reports": total_reports,
#         "completed_reports": completed_reports,
#         "failed_reports": failed_reports,
#         "current_platform": platform
#     }




from database.db import get_db


def get_dashboard_stats(user_id: str):
    conn = get_db()
    cursor = conn.cursor()

    # total reports
    cursor.execute("""
        SELECT COUNT(*) AS total_reports
        FROM reports
        WHERE user_id = %s
    """, (user_id,))
    total_reports = cursor.fetchone()["total_reports"]

    # completed reports
    cursor.execute("""
        SELECT COUNT(*) AS completed_reports
        FROM reports
        WHERE user_id = %s AND status = 'completed'
    """, (user_id,))
    completed_reports = cursor.fetchone()["completed_reports"]

    # failed reports
    cursor.execute("""
        SELECT COUNT(*) AS failed_reports
        FROM reports
        WHERE user_id = %s AND status = 'failed'
    """, (user_id,))
    failed_reports = cursor.fetchone()["failed_reports"]

    # last selected platform
    cursor.execute("""
        SELECT platform
        FROM platform_selection
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    platform = row["platform"] if row else None

    conn.close()

    return {
        "total_reports": total_reports,
        "completed_reports": completed_reports,
        "failed_reports": failed_reports,
        "current_platform": platform
    }
