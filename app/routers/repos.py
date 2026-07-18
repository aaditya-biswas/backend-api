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

import uuid
from urllib.parse import urlparse


from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple,Optional

from fastapi import Request

from app.database import get_db
from app.models import Repo,Job
from app.schemas import RepoCreateRequest, RepoCreateResponse
from app.tasks.ingestion import ingest_repo

router = APIRouter()

'''
        HELPER FUNCTIONS
'''

def _parse_github_url(url:str) -> Tuple[str,str]:
  ''' Extract owner and repo name from the URL '''
  parsed = urlparse(url=url)
  if (parsed.netloc not in ("github.com","www.github.com")):
    raise ValueError("URL must be a github repository")
  path = parsed.path.strip("/")
  
  if path.endswith(".git"):
    path = path[:-4]

  parts = path.split("/")
  if len(parts) < 2 or not parts[0] or not parts[1]:
      raise ValueError("URL must include both owner and repository name")
  return parts[0], parts[1]


@router.post("/", response_model=RepoCreateResponse)
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
    try:
      owner, name = _parse_github_url(body.github_url)
    except ValueError as exc:
      raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail=str(exc))

    # Check if the repo already exists (upsert)
    result = await db.execute(
      select(Repo).where(Repo.owner == owner , Repo.name == name)
    )
    existing_repo = result.scalar_one_or_none()

    if existing_repo is not None:
      repo = existing_repo
    else:
      repo = Repo(
        id=uuid.uuid4(),
        owner=owner,
        name=name,
        github_url = body.github_url,
        status = 'pending'
      )
      db.add(repo)
      await db.flush() # get repo.id before creating Job

    # 3. Create Job record with status = "pending"
    job = Job(
      id = uuid.uuid4(),
      repo_id = repo.id,
      type="ingest",
      status="pending",
      progress=0,
    )

    db.add(job)
    await db.flush()

    ingest_repo.delay(str(repo.id),body.github_url,body.github_token)

    return RepoCreateResponse(
      repo_id = repo.id,
      job_id = job.id,
      status = job.status
    )

