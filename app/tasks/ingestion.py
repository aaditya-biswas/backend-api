"""
Celery tasks for repo ingestion and re-ingestion.

INPUT: repo_id (UUID), github_url, github_token (optional), file_paths (for re-ingest).
OUTPUT: Updates Job records in DB, calls Person 2's Ingestion Service via HTTP.

TASKS:
  - ingest_repo(repo_id, github_url, github_token):
      Calls Person 2's POST /ingest to start full repo ingestion.
      Polls job status or awaits completion.
      Updates the Job record and Repo status.

  - re_ingest_files(repo_id, file_paths):
      Called by webhook handler when files change.
      Calls Person 2's DELETE /ingest/{repo_id}/files then POST /ingest for changed files.

RESOURCES TO LEARN:
- Celery Tasks: https://docs.celeryq.dev/en/stable/userguide/tasks.html
- httpx AsyncClient: https://www.python-httpx.org/async/
- YouTube: "Celery Tasks in Python" - https://www.youtube.com/results?search_query=celery+tasks+python+tutorial
- YouTube: "Async HTTP with httpx" - https://www.youtube.com/results?search_query=python+httpx+async+tutorial
"""

from app.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def ingest_repo(self, repo_id: str, github_url: str, github_token: str = None):
    """
    STUB: Ingest a full GitHub repository via Person 2's service.
    
    TODO:
    1. Update Job status to "running"
    2. Call Person 2's POST /ingest via httpx:
       POST {INGESTION_SERVICE_URL}/ingest
       Body: {"repo_id": repo_id, "github_url": github_url, "github_token": github_token}
    3. Poll or wait for completion
    4. Update Job status to "completed" and Repo status to "ready"
    5. On failure: update Job status to "failed" with error message, retry if appropriate
    """
    raise NotImplementedError("Implement ingest_repo Celery task")


@celery_app.task(bind=True, max_retries=3)
def re_ingest_files(self, repo_id: str, file_paths: list):
    """
    STUB: Re-ingest specific changed files (called by webhook).
    
    TODO:
    1. Call Person 2's DELETE /ingest/{repo_id}/files
       Body: {"file_paths": file_paths}
    2. Call Person 2's POST /ingest with just the changed files
    3. Update Repo commit_sha
    """
    raise NotImplementedError("Implement re_ingest_files Celery task")
