"""Installable command entry points for local hub operation."""
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

from file_intelligence_hub.services.node_health import NodeHealthService
from file_intelligence_hub.storage.db import Database
from file_intelligence_hub.storage.job_repo import JobRepo
from file_intelligence_hub.storage.node_repo import NodeRepo


def api_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the File Intelligence Hub API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args(argv)
    uvicorn = importlib.import_module("uvicorn")
    uvicorn.run("file_intelligence_hub.api.app:app", host=args.host, port=args.port, reload=args.reload)
    return 0


def health_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print local File Intelligence Hub node health")
    parser.add_argument("--db", default=".data/file-intelligence-hub.sqlite3")
    parser.add_argument("--node-id", default="local")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)
    db = Database(args.db)
    service = NodeHealthService(NodeRepo(db.conn), JobRepo(db.conn), node_id=args.node_id, repo_root=Path(args.repo_root))
    print(json.dumps(service.check_local_health(), sort_keys=True))
    return 0
