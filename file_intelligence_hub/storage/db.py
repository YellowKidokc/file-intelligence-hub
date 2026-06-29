"""SQLite connection, schema management, and tiny migrations for the hub ledger."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Callable

SCHEMA_VERSION = 2

BASE_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 100,
    payload_json TEXT NOT NULL,
    result_json TEXT,
    error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL REFERENCES jobs(id),
    status TEXT NOT NULL,
    reason TEXT NOT NULL,
    action TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    decided_at TEXT
);

CREATE TABLE IF NOT EXISTS ledger_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER REFERENCES jobs(id),
    action TEXT NOT NULL,
    before_json TEXT NOT NULL,
    after_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TRIGGER IF NOT EXISTS jobs_updated_at
AFTER UPDATE ON jobs
BEGIN
    UPDATE jobs SET updated_at = datetime('now') WHERE id = NEW.id;
END;
"""

Migration = Callable[[sqlite3.Connection], None]


def _migration_2(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute("INSERT OR IGNORE INTO schema_migrations (version) VALUES (1)")
    conn.execute("INSERT OR IGNORE INTO schema_migrations (version) VALUES (2)")


MIGRATIONS: dict[int, Migration] = {2: _migration_2}


def connect(db_path: str | Path) -> sqlite3.Connection:
    """Open a SQLite connection configured for small local control-plane writes."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def current_version(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT value FROM schema_meta WHERE key = 'schema_version'").fetchone()
    return int(row["value"]) if row else 0


def migrate(conn: sqlite3.Connection, *, target_version: int = SCHEMA_VERSION) -> None:
    version = current_version(conn)
    for next_version in range(version + 1, target_version + 1):
        migration = MIGRATIONS.get(next_version)
        if migration:
            migration(conn)
        conn.execute(
            "INSERT OR REPLACE INTO schema_meta (key, value) VALUES ('schema_version', ?)",
            (str(next_version),),
        )
    conn.commit()


def initialize(conn: sqlite3.Connection) -> None:
    """Create the v1 ledger schema and apply simple forward migrations."""
    conn.executescript(BASE_SCHEMA)
    migrate(conn)


class Database:
    """Tiny connection owner used by scripts, tests, and API handlers."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.conn = connect(self.db_path)
        initialize(self.conn)

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
