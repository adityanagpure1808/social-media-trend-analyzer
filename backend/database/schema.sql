-- reports table (already exists)
-- platform_selection table (already exists)

CREATE TABLE IF NOT EXISTS report_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id TEXT NOT NULL,
    user_id TEXT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'rag',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
