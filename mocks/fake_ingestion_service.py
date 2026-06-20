"""
Mock Ingestion Service — matches Person 2's contract exactly.

Run this on a separate port (e.g., 8002) so Person 3 can develop
the full orchestration logic before Person 2's real service is ready.

INPUT: POST /search, POST /ingest, DELETE /ingest/{repo_id}/files
OUTPUT: Canned responses matching Person 2's chunk schema.

USAGE:
  uvicorn mocks.fake_ingestion_service:app --port 8002

RESOURCES TO LEARN:
- FastAPI Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/
- Pydantic Models: https://docs.pydantic.dev/latest/
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Fake Ingestion Service")


class SearchRequest(BaseModel):
    repo_id: str
    query: str
    top_k: int = 6


class IngestRequest(BaseModel):
    repo_id: str
    github_url: str
    github_token: str = None


class DeleteFilesRequest(BaseModel):
    file_paths: list[str]


@app.post("/ingest")
async def fake_ingest(body: IngestRequest):
    """Returns a canned 'started' response."""
    return {"status": "started", "repo_id": body.repo_id}


@app.post("/search")
async def fake_search(body: SearchRequest):
    """Returns a canned search result matching the chunk schema."""
    return {
        "chunks": [
            {
                "text": "def example_function():\n    '''An example function for testing.'''\n    pass",
                "file_path": "src/example.py",
                "start_line": 1,
                "end_line": 4,
                "language": "python",
                "chunk_type": "function",
                "score": 0.95,
            },
            {
                "text": "class ExampleClass:\n    def method(self):\n        return 'hello'",
                "file_path": "src/example.py",
                "start_line": 6,
                "end_line": 9,
                "language": "python",
                "chunk_type": "class",
                "score": 0.89,
            },
        ]
    }


@app.delete("/ingest/{repo_id}/files")
async def fake_delete_files(repo_id: str, body: DeleteFilesRequest):
    """Returns a canned 'deleted' response."""
    return {"status": "deleted", "repo_id": repo_id, "files_deleted": len(body.file_paths)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
