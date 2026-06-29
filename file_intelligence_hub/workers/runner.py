"""Intentional worker queue runner for queued hub jobs."""
from __future__ import annotations

import argparse
import time
from pathlib import Path

from file_intelligence_hub.core.job_manager import JobManager
from file_intelligence_hub.storage.db import Database
from file_intelligence_hub.storage.job_repo import JobRepo


class WorkerRunner:
    def __init__(self, repo: JobRepo) -> None:
        self.repo = repo
        self.manager = JobManager(repo)

    def process_next(self) -> dict[str, object] | None:
        job = self.repo.next_queued_job()
        if not job:
            return None
        if job["type"] == "file_event":
            return self.manager.process_file_event(job["id"])
        return self.repo.update_job(job["id"], status="failed", error=f"unsupported job type: {job['type']}")

    def run_once(self, *, limit: int | None = None) -> list[dict[str, object]]:
        processed: list[dict[str, object]] = []
        while limit is None or len(processed) < limit:
            result = self.process_next()
            if result is None:
                break
            processed.append(result)
        return processed

    def run_forever(self, *, interval: float = 1.0) -> None:
        while True:
            self.run_once(limit=1)
            time.sleep(interval)


def build_runner(db_path: str | Path) -> WorkerRunner:
    db = Database(db_path)
    return WorkerRunner(JobRepo(db.conn))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process queued file intelligence hub jobs")
    parser.add_argument("--db", default=".data/file-intelligence-hub.sqlite3")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--forever", action="store_true")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args(argv)

    runner = build_runner(args.db)
    if args.forever:
        runner.run_forever(interval=args.interval)
    else:
        runner.run_once(limit=args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
