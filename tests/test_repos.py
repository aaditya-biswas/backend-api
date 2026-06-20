"""
Tests for POST /repos and GET /jobs/{id} endpoints.

INPUT: Test client requests.
OUTPUT: Assertions on response status codes, shapes, and DB state.

RESOURCES TO LEARN:
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- httpx AsyncClient: https://www.python-httpx.org/advanced/#testing
- YouTube: "Testing FastAPI Applications" - https://www.youtube.com/results?search_query=testing+fastapi+pytest+async
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    """Create an async test client."""
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_create_repo():
    """
    STUB: Test POST /repos.
    
    TODO:
    1. Send POST /repos with valid github_url
    2. Assert 200 response
    3. Assert response contains repo_id, job_id, status
    4. Assert a Job record was created in DB
    """
    raise NotImplementedError("Implement test_create_repo")


@pytest.mark.asyncio
async def test_get_job_status():
    """
    STUB: Test GET /jobs/{id}.
    
    TODO:
    1. Create a repo first (to get a job_id)
    2. GET /jobs/{job_id}
    3. Assert 200 response with correct status field
    4. Test 404 for non-existent job
    """
    raise NotImplementedError("Implement test_get_job_status")
