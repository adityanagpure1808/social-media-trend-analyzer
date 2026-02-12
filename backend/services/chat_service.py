




# from datetime import datetime
# from database.db import get_db


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



# from datetime import datetime
# import sqlite3
# import time
# from database.db import get_db


# # =====================================================
# # SAFE WRITE (with retry)
# # =====================================================
# def save_chat_message(user_id, report_id, question, answer, source, retries=3):

#     for attempt in range(retries):
#         try:
#             conn = get_db()
#             cursor = conn.cursor()

#             cursor.execute("""
#                 INSERT INTO report_chat (
#                     user_id,
#                     report_id,
#                     question,
#                     answer,
#                     source,
#                     created_at
#                 )
#                 VALUES (?, ?, ?, ?, ?, ?)
#             """, (
#                 user_id,
#                 report_id,
#                 question,
#                 answer,
#                 source,
#                 datetime.utcnow().isoformat()
#             ))

#             conn.commit()
#             conn.close()
#             return True

#         except sqlite3.OperationalError as e:
#             if "locked" in str(e).lower() and attempt < retries - 1:
#                 time.sleep(0.2)  # wait and retry
#             else:
#                 print("DB write failed:", e)
#                 return False


# # =====================================================
# # SAFE HISTORY FETCH
# # =====================================================
# def get_chat_history(report_id: str, limit: int = 50):
#     """
#     Returns last N messages only (prevents huge payloads)
#     """

#     try:
#         conn = get_db()
#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT question, answer, source, created_at
#             FROM report_chat
#             WHERE report_id = ?
#             ORDER BY id DESC
#             LIMIT ?
#         """, (report_id, limit))

#         rows = cursor.fetchall()
#         conn.close()

#         # reverse to chronological order
#         return [dict(row) for row in reversed(rows)]

#     except Exception as e:
#         print("History fetch failed:", e)
#         return []




from datetime import datetime
from database.db import get_db


# =====================================================
# SAVE CHAT MESSAGE
# =====================================================
def save_chat_message(user_id, report_id, question, answer, source):

    try:
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
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            report_id,
            question,
            answer,
            source,
            datetime.utcnow()
        ))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print("DB write failed:", e)
        return False


# =====================================================
# FETCH CHAT HISTORY
# =====================================================
def get_chat_history(report_id: str, limit: int = 50):
    """
    Returns last N messages only (chronological order)
    """

    try:
        conn = get_db()
        cursor = conn.cursor()

        # IMPORTANT: ORDER BEFORE LIMIT and LIMIT cannot be parameterized
        cursor.execute(f"""
            SELECT question, answer, source, created_at
            FROM report_chat
            WHERE report_id = %s
            ORDER BY id DESC
            LIMIT {int(limit)}
        """, (report_id,))

        rows = cursor.fetchall()
        conn.close()

        # convert to chronological order
        return [dict(row) for row in reversed(rows)]

    except Exception as e:
        print("History fetch failed:", e)
        return []
