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

from app.config import settings
from app.schemas import CodeChunk


async def ingest_repo(repo_id: str, github_url: str, github_token: str = None) -> dict:
    """
    STUB: Tell Person 2's service to ingest a repo.
    
    INPUT: repo_id, github_url, optional github_token.
    OUTPUT: {"status": "started"} from ingestion service.
    
    TODO:
    1. POST {INGESTION_SERVICE_URL}/ingest
       Body: {"repo_id": repo_id, "github_url": github_url, "github_token": github_token}
    2. Return response JSON
    """
    raise NotImplementedError("Implement ingestion_client.ingest_repo")


async def search(repo_id: str, query: str, top_k: int = 6) -> list[CodeChunk]:
    """
    STUB: Search for relevant code chunks.
    
    INPUT: repo_id to search in, natural language query, number of results (top_k).
    OUTPUT: List of CodeChunk objects sorted by relevance score.
    
    TODO:
    1. POST {INGESTION_SERVICE_URL}/search
       Body: {"repo_id": repo_id, "query": query, "top_k": top_k}
    2. Parse response chunks into CodeChunk objects
    3. Return sorted list by score descending
    """
    raise NotImplementedError("Implement ingestion_client.search")


async def delete_files(repo_id: str, file_paths: list[str]) -> dict:
    """
    STUB: Delete specific files from the index.
    
    INPUT: repo_id, list of file paths to remove.
    OUTPUT: {"status": "deleted"} from ingestion service.
    
    TODO:
    1. DELETE {INGESTION_SERVICE_URL}/ingest/{repo_id}/files
       Body: {"file_paths": file_paths}
    2. Return response JSON
    """
    raise NotImplementedError("Implement ingestion_client.delete_files")
