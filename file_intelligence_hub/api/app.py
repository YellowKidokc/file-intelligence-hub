"""Minimal FastAPI app factory for local development."""
from __future__ import annotations

from fastapi import FastAPI

from file_intelligence_hub.api.routes_intelligence import router as intelligence_router
from file_intelligence_hub.api.routes_jobs import router as jobs_router
from file_intelligence_hub.api.routes_nodes import router as nodes_router


def create_app() -> FastAPI:
    app = FastAPI(title="File Intelligence Hub", version="0.1.0")
    app.include_router(jobs_router)
    app.include_router(intelligence_router)
    app.include_router(nodes_router)
    return app


app = create_app()
