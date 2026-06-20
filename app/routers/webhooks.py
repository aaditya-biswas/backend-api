"""
POST /webhooks/github — Receive GitHub push events for auto-reindex.

INPUT: GitHub webhook payload (JSON) + X-Hub-Signature-256 header
  - The payload contains ref, before/after commit SHAs, and changed files
  - The signature is HMAC-SHA256 of the body using the SECRET_KEY

OUTPUT: 200 OK (acknowledgment)
  - The actual re-ingestion happens asynchronously via Celery

FLOW:
  1. Verify X-Hub-Signature-256 using hmac.compare_digest (constant-time)
  2. Check X-GitHub-Delivery against a Redis set for idempotency
  3. Extract changed files from the push payload
  4. Enqueue a re_ingest_files Celery task that:
     a. Calls Person 2's DELETE /ingest/{repo_id}/files for changed files
     b. Calls Person 2's POST /ingest for just the changed files
  5. Return 200

RESOURCES TO LEARN:
- GitHub Webhooks: https://docs.github.com/en/webhooks
- HMAC Verification: https://docs.python.org/3/library/hmac.html
- YouTube: "GitHub Webhooks with FastAPI" - https://www.youtube.com/results?search_query=github+webhooks+fastapi+python
- YouTube: "Webhook Security Best Practices" - https://www.youtube.com/results?search_query=webhook+security+hmac+verification
"""

from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/github")
async def github_webhook(request: Request):
    """
    STUB: Handle GitHub push event webhooks.
    
    TODO:
    1. Read raw body: body = await request.body()
    2. Get signature from header: request.headers.get("x-hub-signature-256")
    3. Verify HMAC-SHA256 using SECRET_KEY and hmac.compare_digest
    4. Check idempotency: verify X-GitHub-Delivery not already processed (Redis SET)
    5. Parse JSON payload
    6. Extract changed files from commits
    7. Look up repo by full_name in DB
    8. Enqueue Celery task: re_ingest_files.delay(repo_id, changed_files)
    9. Return {"status": "ok"}
    """
    raise NotImplementedError("Implement POST /webhooks/github")
