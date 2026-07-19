"""
HTTP client for Person 2's Ingestion Service.

INPUT: repo_id, github_url, github_token, query, file_paths (depending on the method).
OUTPUT: Search results or ingestion status.

METHODS:
  - ingest_repo(repo_id, github_url, github_token):
      Calls POST /ingest to start full repo ingestion.
      
  - search(repo_id, query, top_k=6):
      Calls POST /search to find relevant code chunks.
      Returns list of CodeChunk objects.
      
  - delete_files(repo_id, file_paths):
      Calls DELETE /ingest/{repo_id}/files to remove specific files.

RESOURCES TO LEARN:
- httpx AsyncClient: https://www.python-httpx.org/async/
- FastAPI Test Client: https://fastapi.tiangolo.com/tutorial/testing/
- YouTube: "Python httpx Tutorial" - https://www.youtube.com/results?search_query=python+httpx+async+client+tutorial
"""

import httpx
from app.config import settings
from app.schemas import CodeChunk

# Shared AsyncClient with connection pooling (lazy-initialised)
_ingestion_client: httpx.AsyncClient | None = None


async def get_client() -> httpx.AsyncClient:
    """Return the shared AsyncClient, creating it on first call."""
    global _ingestion_client
    if _ingestion_client is None:
        _ingestion_client = httpx.AsyncClient(
            base_url=settings.INGESTION_SERVICE_URL,
            timeout=300.0,
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
                keepalive_expiry=30.0,
            ),
        )
    return _ingestion_client


async def ingest_repo(repo_id: str, github_url: str, github_token: str | None = None) -> dict:
    """
    Tell Person 2's service to ingest a repo.
    
    INPUT: repo_id, github_url, optional github_token.
    OUTPUT: {"status": "started"} from ingestion service.
    
    1. POST {INGESTION_SERVICE_URL}/ingest
       Body: {"repo_id": repo_id, "github_url": github_url, "github_token": github_token}
    2. Return response JSON
    """
    client = await get_client()
    resp = await client.post("/ingest", json={
        "repo_id": repo_id,
        "github_url": github_url,
        "github_token": github_token,
    })
    resp.raise_for_status()
    return resp.json()


async def search(repo_id: str, query: str, top_k: int = 6) -> list[CodeChunk]:
    """
    Search for relevant code chunks.
    
    INPUT: repo_id to search in, natural language query, number of results (top_k).
    OUTPUT: List of CodeChunk objects sorted by relevance score.
    
    1. POST {INGESTION_SERVICE_URL}/search
       Body: {"repo_id": repo_id, "query": query, "top_k": top_k}
    2. Parse response chunks into CodeChunk objects
    3. Return sorted list by score descending
    """
    client = await get_client()
    resp = await client.post(
        "/search",
        json={
            "repo_id": repo_id,
            "query": query,
            "top_k": top_k,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    chunks = [CodeChunk(**item) for item in data]
    chunks.sort(key=lambda c: c.score, reverse=True)
    return chunks


async def delete_files(repo_id: str, file_paths: list[str]) -> dict:
    """
    Delete specific files from the index.
    
    INPUT: repo_id, list of file paths to remove.
    OUTPUT: {"status": "deleted"} from ingestion service.
    
    1. DELETE {INGESTION_SERVICE_URL}/ingest/{repo_id}/files
       Body: {"file_paths": file_paths}
    2. Return response JSON
    """
    client = await get_client()
    resp = await client.delete(
        f"/ingest/{repo_id}/files",
        json={"file_paths": file_paths},
    )
    resp.raise_for_status()
    return resp.json()
