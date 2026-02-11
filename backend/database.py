import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS platform_selections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    platform TEXT,
    selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
