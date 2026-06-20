"""
FastAPI application entry point.

RESOURCES TO LEARN:
- FastAPI Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- FastAPI Bigger Applications: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- YouTube: "FastAPI Full Course" by FreeCodeCamp - https://www.youtube.com/results?search_query=fastapi+full+course+python
- YouTube: "FastAPI for Beginners" - https://www.youtube.com/results?search_query=fastapi+for+beginners
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import repos, jobs, query, webhooks
from app.middleware.auth import APIKeyMiddleware

app = FastAPI(
    title="Codebase Q&A - Backend Orchestration API",
    description="Orchestrates ingestion, search, and LLM querying for the Codebase Q&A system.",
    version="0.1.0",
    docs_url="/docs",
)

# CORS - allow VS Code extension to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication middleware
app.add_middleware(APIKeyMiddleware)

# Include routers
app.include_router(repos.router, prefix="/repos", tags=["Repos"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(query.router, prefix="/query", tags=["Query"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
