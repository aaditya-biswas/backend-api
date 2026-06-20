"""
GET /jobs/{id} — Poll the status of an async job.

INPUT: job_id (UUID path parameter)
  - The UUID returned from POST /repos

OUTPUT: JobStatusResponse {id, repo_id, type, status, progress, error, created_at, updated_at}
  - status: "pending" | "running" | "completed" | "failed"
  - progress: 0-100 percentage
  - error: Error message if failed, null otherwise

FLOW:
  1. Look up the Job by ID in Postgres
  2. Return its current status
  3. The Celery worker updates this record as it progresses

RESOURCES TO LEARN:
- FastAPI Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/
- SQLAlchemy Async Queries: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- YouTube: "FastAPI Path and Query Parameters" - https://www.youtube.com/results?search_query=fastapi+path+parameters+tutorial
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Job
from app.schemas import JobStatusResponse

router = APIRouter()


@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    STUB: Get the status of an async job.
    
    TODO:
    1. Query Job table by job_id
    2. If not found, raise 404
    3. Return job status
    """
    raise NotImplementedError("Implement GET /jobs/{id}")
