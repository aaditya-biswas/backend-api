"""
Pydantic v2 schemas for request/response validation.

INPUT: Raw HTTP request bodies.
OUTPUT: Validated, typed Python objects that FastAPI injects into route handlers.

RESOURCES TO LEARN:
- Pydantic v2 Docs: https://docs.pydantic.dev/latest/
- FastAPI Request Body: https://fastapi.tiangolo.com/tutorial/body/
- YouTube: "Pydantic v2 Complete Guide" - https://www.youtube.com/results?search_query=pydantic+v2+tutorial+python
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


# ─── Repos ───

class RepoCreateRequest(BaseModel):
    """POST /repos request body.
    INPUT: github_url (the repo URL) and optional github_token for private repos.
    """
    github_url: str = Field(..., description="Full GitHub repository URL")
    github_token: Optional[str] = Field(None, description="GitHub token for private repos")


class RepoCreateResponse(BaseModel):
    """POST /repos response body.
    OUTPUT: repo_id (UUID), job_id (UUID for tracking), and initial status.
    """
    repo_id: UUID
    job_id: UUID
    status: str


# ─── Jobs ───

class JobStatusResponse(BaseModel):
    """GET /jobs/{id} response body.
    OUTPUT: Current job status, progress percentage, and error message if failed.
    """
    id: UUID
    repo_id: UUID
    type: str
    status: str
    progress: int
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# ─── Query ───

class QueryRequest(BaseModel):
    """POST /query request body.
    INPUT: repo_id to search within, the natural-language question, and whether to stream.
    """
    repo_id: UUID = Field(..., description="ID of the ingested repo to query")
    question: str = Field(..., description="Natural language question about the codebase")
    stream: bool = Field(True, description="Whether to stream the answer via SSE")


# ─── Webhook ───

class WebhookPayload(BaseModel):
    """GitHub webhook push event payload.
    INPUT: GitHub sends this automatically on push events.
    """
    ref: str
    before: str
    after: str
    repository: dict
    commits: list = []


# ─── Chunk Schema (shared contract with Person 2) ───

class CodeChunk(BaseModel):
    """A single code chunk returned by Person 2's Ingestion Service.
    This is the MOST IMPORTANT shared contract in the project.
    Person 3 builds prompt assembly logic directly against these field names.
    """
    text: str
    file_path: str
    start_line: int
    end_line: int
    language: str
    chunk_type: str  # function, class, module
    score: float
