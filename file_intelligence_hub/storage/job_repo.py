"""Repository methods for jobs, review items, and ledger entries."""
from __future__ import annotations

import json
import sqlite3
from typing import Any

JsonDict = dict[str, Any]


def _dump(value: JsonDict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _load(value: str | None) -> JsonDict | None:
    return json.loads(value) if value else None


def _job(row: sqlite3.Row) -> JsonDict:
    return {
        "id": row["id"],
        "type": row["type"],
        "status": row["status"],
        "priority": row["priority"],
        "payload": _load(row["payload_json"]),
        "result": _load(row["result_json"]),
        "error": row["error"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


class JobRepo:
    """Persistence boundary for the hub brain."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def create_job(self, job_type: str, payload: JsonDict, *, priority: int = 100) -> JsonDict:
        cur = self.conn.execute(
            "INSERT INTO jobs (type, status, priority, payload_json) VALUES (?, 'queued', ?, ?)",
            (job_type, priority, _dump(payload)),
        )
        self.conn.commit()
        return self.get_job(int(cur.lastrowid))

    def get_job(self, job_id: int) -> JsonDict:
        row = self.conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(f"job {job_id} not found")
        return _job(row)

    def list_jobs(self, *, status: str | None = None) -> list[JsonDict]:
        if status:
            rows = self.conn.execute("SELECT * FROM jobs WHERE status = ? ORDER BY id", (status,)).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM jobs ORDER BY id").fetchall()
        return [_job(row) for row in rows]

    def update_job(self, job_id: int, *, status: str, result: JsonDict | None = None, error: str | None = None) -> JsonDict:
        self.conn.execute(
            "UPDATE jobs SET status = ?, result_json = ?, error = ? WHERE id = ?",
            (status, _dump(result) if result is not None else None, error, job_id),
        )
        self.conn.commit()
        return self.get_job(job_id)

    def create_review_item(self, job_id: int, *, reason: str, action: str, payload: JsonDict) -> JsonDict:
        cur = self.conn.execute(
            """
            INSERT INTO review_items (job_id, status, reason, action, payload_json)
            VALUES (?, 'pending', ?, ?, ?)
            """,
            (job_id, reason, action, _dump(payload)),
        )
        self.conn.commit()
        return self.get_review_item(int(cur.lastrowid))

    def get_review_item(self, review_id: int) -> JsonDict:
        row = self.conn.execute("SELECT * FROM review_items WHERE id = ?", (review_id,)).fetchone()
        if row is None:
            raise KeyError(f"review item {review_id} not found")
        return {
            "id": row["id"], "job_id": row["job_id"], "status": row["status"],
            "reason": row["reason"], "action": row["action"], "payload": _load(row["payload_json"]),
            "created_at": row["created_at"], "decided_at": row["decided_at"],
        }

    def list_review_items(self, *, status: str | None = None) -> list[JsonDict]:
        sql = "SELECT * FROM review_items" + (" WHERE status = ?" if status else "") + " ORDER BY id"
        rows = self.conn.execute(sql, (status,) if status else ()).fetchall()
        return [self.get_review_item(row["id"]) for row in rows]

    def next_queued_job(self) -> JsonDict | None:
        row = self.conn.execute(
            "SELECT * FROM jobs WHERE status = 'queued' ORDER BY priority ASC, id ASC LIMIT 1"
        ).fetchone()
        return _job(row) if row else None

    def decide_review_item(self, review_id: int, status: str) -> JsonDict:
        if status not in {"approved", "rejected", "deferred"}:
            raise ValueError("review status must be approved, rejected, or deferred")
        self.conn.execute(
            "UPDATE review_items SET status = ?, decided_at = datetime('now') WHERE id = ?",
            (status, review_id),
        )
        self.conn.commit()
        return self.get_review_item(review_id)

    def add_ledger_entry(self, *, job_id: int | None, action: str, before: JsonDict, after: JsonDict) -> JsonDict:
        cur = self.conn.execute(
            "INSERT INTO ledger_entries (job_id, action, before_json, after_json) VALUES (?, ?, ?, ?)",
            (job_id, action, _dump(before), _dump(after)),
        )
        self.conn.commit()
        row = self.conn.execute("SELECT * FROM ledger_entries WHERE id = ?", (cur.lastrowid,)).fetchone()
        return {"id": row["id"], "job_id": row["job_id"], "action": row["action"], "before": _load(row["before_json"]), "after": _load(row["after_json"]), "created_at": row["created_at"]}
