"""Apply approved review decisions."""
from __future__ import annotations

from file_intelligence_hub.storage.job_repo import JobRepo
from file_intelligence_hub.workers.rename_worker import execute_rename


def apply_approved_review(repo: JobRepo, review_id: int) -> dict[str, object]:
    review = repo.get_review_item(review_id)
    if review["status"] != "approved":
        raise ValueError("review item must be approved before execution")
    if review["action"] != "rename":
        raise ValueError(f"unsupported review action {review['action']}")
    before = {"path": review["payload"]["source_path"]}
    result = execute_rename(review["payload"])
    repo.add_ledger_entry(job_id=review["job_id"], action="rename", before=before, after=result)
    repo.update_job(review["job_id"], status="completed", result=result)
    return result
