"""
POST /repos — Register a GitHub repo for ingestion.

INPUT: RepoCreateRequest {github_url, github_token}
  - github_url: Full URL of the GitHub repo to ingest
  - github_token: Optional token for private repos

OUTPUT: RepoCreateResponse {repo_id, job_id, status}
  - repo_id: UUID of the created repo record
  - job_id: UUID of the Celery job that will ingest it
  - status: "pending" initially

FLOW:
  1. Validate the GitHub URL
  2. Create a Repo record in Postgres
  3. Enqueue a Celery task (ingest_repo) that calls Person 2's /ingest
  4. Return the repo_id and job_id immediately

RESOURCES TO LEARN:
- FastAPI Routers: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- FastAPI Path Operations: https://fastapi.tiangolo.com/tutorial/path-params/
- YouTube: "FastAPI Routers and Modular Apps" - https://www.youtube.com/results?search_query=fastapi+routers+modular+application
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import RepoCreateRequest, RepoCreateResponse

router = APIRouter()


@router.post("", response_model=RepoCreateResponse)
async def create_repo(body: RepoCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    STUB: Register a repo for ingestion.
    
    TODO:
    1. Parse owner/name from github_url
    2. Check if repo already exists (upsert logic)
    3. Create Repo record in DB
    4. Create Job record with status="pending"
    5. Enqueue Celery task: ingest_repo.delay(repo_id, github_url, github_token)
    6. Return repo_id and job_id
    """
    raise NotImplementedError("Implement POST /repos")
