"""Small FastAPI router for job intake and review decisions."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from file_intelligence_hub.core.job_manager import JobManager
from file_intelligence_hub.storage.db import Database
from file_intelligence_hub.storage.job_repo import JobRepo
from file_intelligence_hub.workers.review_worker import apply_approved_review

DEFAULT_DB_PATH = Path(os.environ.get("FIHUB_DB_PATH", ".data/file-intelligence-hub.sqlite3"))
router = APIRouter(tags=["control-plane"])


class FileEventRequest(BaseModel):
    event_type: str = Field(default="created")
    path: str
    is_directory: bool = False
    dest_path: str | None = None
    source: str = "api"


class ReviewDecisionRequest(BaseModel):
    status: Literal["approved", "rejected", "deferred"]


def _repo() -> JobRepo:
    db = Database(DEFAULT_DB_PATH)
    return JobRepo(db.conn)


@router.post("/jobs/file-events")
def create_file_event(request: FileEventRequest) -> dict[str, object]:
    repo = _repo()
    manager = JobManager(repo)
    return manager.ingest_file_event(request.model_dump(exclude={"source"}, exclude_none=True), source=request.source)


@router.get("/jobs")
def list_jobs(status: str | None = None) -> dict[str, object]:
    return {"jobs": _repo().list_jobs(status=status)}


@router.get("/reviews")
def list_reviews(status: str | None = None) -> dict[str, object]:
    return {"review_items": _repo().list_review_items(status=status)}


@router.get("/reviews/{review_id}")
def get_review(review_id: int) -> dict[str, object]:
    try:
        return {"review_item": _repo().get_review_item(review_id)}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/reviews/{review_id}/decision")
def decide_review(review_id: int, request: ReviewDecisionRequest) -> dict[str, object]:
    repo = _repo()
    try:
        review = repo.decide_review_item(review_id, request.status)
        result = apply_approved_review(repo, review_id) if request.status == "approved" else {"review": review}
        return {"review": review, "result": result}
    except (KeyError, ValueError, FileNotFoundError, FileExistsError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/reviews/{review_id}/approve")
def approve_review(review_id: int) -> dict[str, object]:
    return decide_review(review_id, ReviewDecisionRequest(status="approved"))


@router.post("/reviews/{review_id}/reject")
def reject_review(review_id: int) -> dict[str, object]:
    return decide_review(review_id, ReviewDecisionRequest(status="rejected"))


@router.post("/reviews/{review_id}/defer")
def defer_review(review_id: int) -> dict[str, object]:
    return decide_review(review_id, ReviewDecisionRequest(status="deferred"))
