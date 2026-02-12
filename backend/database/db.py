# # import sqlite3
# # import os

# # DB_PATH = os.getenv("DB_PATH", "database.db")

# # def get_db():
# #     conn = sqlite3.connect(DB_PATH, check_same_thread=False)
# #     conn.row_factory = sqlite3.Row
# #     return conn



# import sqlite3
# import os
# from pathlib import Path

# # =====================================================
# # PERSISTENT STORAGE (Render Disk)
# # =====================================================
# # Render provides persistent disk at /data
# DATA_DIR = os.getenv("RENDER_DISK_PATH", "/data")

# Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# DB_PATH = os.path.join(DATA_DIR, "database.db")


# # =====================================================
# # CONNECTION FACTORY
# # =====================================================
# def get_db():
#     conn = sqlite3.connect(
#         DB_PATH,
#         check_same_thread=False,
#         timeout=30,  # prevents "database is locked"
#     )

#     conn.row_factory = sqlite3.Row

#     # WAL MODE = allows reads during writes (VERY IMPORTANT)
#     conn.execute("PRAGMA journal_mode=WAL;")
#     conn.execute("PRAGMA synchronous=NORMAL;")
#     conn.execute("PRAGMA foreign_keys=ON;")

#     return conn





import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")

_conn = None

def get_db():
    """
    Returns reusable Supabase Postgres connection.
    Automatically reconnects if Render sleeps.
    """
    global _conn

    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL not set in environment variables")

    try:
        if _conn is None or _conn.closed != 0:
            _conn = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=RealDictCursor,
                sslmode="require"
            )
        return _conn

    except Exception as e:
        print("Reconnecting to database:", e)
        _conn = psycopg2.connect(
            DATABASE_URL,
            cursor_factory=RealDictCursor,
            sslmode="require"
        )
        return _conn
