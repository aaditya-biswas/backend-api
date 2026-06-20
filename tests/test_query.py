"""
Tests for POST /query endpoint.

INPUT: Test client requests with repo_id and question.
OUTPUT: Assertions on SSE streaming response.

RESOURCES TO LEARN:
- SSE Testing: https://github.com/sysid/sse-starlette
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/
- YouTube: "Testing Streaming Endpoints" - https://www.youtube.com/results?search_query=testing+sse+streaming+fastapi
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_query_repo():
    """
    STUB: Test POST /query with streaming.
    
    TODO:
    1. Send POST /query with valid repo_id and question
    2. Assert 200 response with media_type "text/event-stream"
    3. Collect SSE events
    4. Assert at least one data chunk received
    5. Assert final [DONE] event received
    """
    raise NotImplementedError("Implement test_query_repo")
