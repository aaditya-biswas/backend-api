"""
Tests for POST /webhooks/github endpoint.

INPUT: Simulated GitHub webhook payload with HMAC signature.
OUTPUT: Assertions on webhook verification and task enqueueing.

RESOURCES TO LEARN:
- GitHub Webhook Payloads: https://docs.github.com/en/webhooks/webhook-events-and-payloads#push
- HMAC in Python: https://docs.python.org/3/library/hmac.html
- YouTube: "Webhook Testing Strategies" - https://www.youtube.com/results?search_query=webhook+testing+python+hmac
"""

import hmac
import hashlib
import json
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings


def sign_payload(payload: dict, secret: str) -> str:
    """Create X-Hub-Signature-256 for a payload."""
    body = json.dumps(payload).encode()
    signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={signature}"


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_webhook_valid_signature():
    """
    STUB: Test webhook with valid HMAC signature.
    
    TODO:
    1. Create a realistic push event payload
    2. Sign it with SECRET_KEY
    3. POST /webhooks/github with payload + signature header
    4. Assert 200 response
    """
    raise NotImplementedError("Implement test_webhook_valid_signature")


@pytest.mark.asyncio
async def test_webhook_invalid_signature():
    """
    STUB: Test webhook with invalid HMAC signature (should reject).
    
    TODO:
    1. Create a payload
    2. Sign it with WRONG secret
    3. POST /webhooks/github
    4. Assert 403 response
    """
    raise NotImplementedError("Implement test_webhook_invalid_signature")
