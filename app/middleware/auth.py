"""
API Key authentication middleware.

INPUT: HTTP Request with X-API-Key header.
OUTPUT: 403 Forbidden if key is invalid, passes through to route if valid.

FLOW:
  1. Extract X-API-Key from request headers
  2. Compare against configured API_KEY (from env)
  3. If mismatch, return 403 JSON response
  4. If match, let request proceed

RESOURCES TO LEARN:
- FastAPI Middleware: https://fastapi.tiangolo.com/tutorial/middleware/
- FastAPI Dependencies for Auth: https://fastapi.tiangolo.com/tutorial/security/
- YouTube: "FastAPI Authentication" - https://www.youtube.com/results?search_query=fastapi+api+key+authentication+middleware
- slowapi rate limiting: https://github.com/laurentS/slowapi
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Validates X-API-Key header on every request except /health and /docs."""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for health check, docs, and webhooks (GitHub can't send custom headers easily)
        if request.url.path in ["/health", "/docs", "/openapi.json"] or request.url.path.startswith("/webhooks"):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key != settings.API_KEY:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid or missing API key. Provide X-API-Key header."},
            )

        return await call_next(request)
