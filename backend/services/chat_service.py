

# from datetime import datetime
# from database.connection import get_db

# def save_chat_message(user_id, report_id, question, answer, source):
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute("""
#     INSERT INTO report_chat (
#         user_id,
#         report_id,
#         question,
#         answer,
#         source,
#         created_at
#     )
#     VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         user_id,
#         report_id,
#         question,
#         answer,
#         source,
#         datetime.utcnow().isoformat()
#     ))

#     conn.commit()
#     conn.close()





# def get_chat_history(report_id: str):
#     conn = get_db()
#     cursor = conn.cursor()

#     try:
#         cursor.execute("""
#             SELECT question, answer, source, created_at
#             FROM report_chat
#             WHERE report_id = ?
#             ORDER BY id ASC
#         """, (report_id,))

#         rows = cursor.fetchall()
#         return [dict(row) for row in rows]

#     except Exception:
#         return []

#     finally:
#         conn.close()




from datetime import datetime
from database.db import get_db


def save_chat_message(user_id, report_id, question, answer, source):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO report_chat (
        user_id,
        report_id,
        question,
        answer,
        source,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        report_id,
        question,
        answer,
        source,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def get_chat_history(report_id: str):
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT question, answer, source, created_at
            FROM report_chat
            WHERE report_id = ?
            ORDER BY id ASC
        """, (report_id,))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except Exception:
        return []

    finally:
        conn.close()
