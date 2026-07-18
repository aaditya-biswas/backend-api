# Person 3 — Backend Orchestration API: Step-by-Step Plan

**Your Role:** Build the central orchestration API that connects Person 1 (LLM), Person 2 (Ingestion), and Person 4 (VS Code Extension).

**Repository:** [`backend-api/`](backend-api/)

---

## Local Dev Environment Setup (Do This First)

You need **Postgres** (database), **Redis** (Celery broker), and **Python 3.11+** running on your machine. The easiest way is Docker.

### Step 1: Start Postgres (Docker)

```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=backend_api \
  -p 5432:5432 \
  -d postgres:16
```

This runs Postgres 16 in the background, exposed on port `5432`. The connection string becomes:
```
postgresql+asyncpg://postgres:postgres@localhost:5432/backend_api
```

### Step 2: Start Redis (Docker)

```bash
docker run --name redis \
  -p 6379:6379 \
  -d redis:7
```

Redis runs on port `6379` — Celery uses this as its broker.

### Step 3: Verify Both Are Running

```bash
docker ps
# You should see both "postgres" and "redis" containers with "Up" status
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env
# The defaults in .env already match the Docker Postgres/Redis above
```

### Step 5: Run Database Migrations

```bash
alembic upgrade head
```

### Step 6: Start the API

```bash
uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

### Stopping & Cleaning Up

```bash
# Stop containers
docker stop postgres redis

# Remove containers (data is lost)
docker rm postgres redis

# To persist data, add -v flags:
# docker run --name postgres -v postgres_data:/var/lib/postgresql/data ...
```

---

## Step-by-Step Execution Plan

### Phase 0: Day 1 — Kickoff & Contracts (Coordinate with Team)

| # | Task | Details | Est. Time |
|---|------|---------|-----------|
| 0.1 | **Join the contracts call** | Agree on `API_CONTRACTS.md` with all 4 people. Lock in: (a) Person 1's `/v1/chat/completions` shape, (b) Person 2's chunk schema (field names/types), (c) Docker network name & port numbers. **Nobody writes code until this is done.** | 2 hrs |
| 0.2 | **Confirm Docker names with Person 4** | Agree on container name (`backend-api`), port (`8000`), and shared network name. | 30 min |

### Phase 1: Week 1 — Scaffolding, DB, Auth, Mocks

| # | Task | Files to Implement | What It Does | Est. Time |
|---|------|-------------------|-------------|-----------|
| 1.1 | **Set up dev environment** | — | Run Postgres + Redis via Docker (see setup section above). Install Python deps. | 1 hr |
| 1.2 | **Implement config** | [`app/config.py`](backend-api/app/config.py) | Reads env vars via Pydantic Settings. **Input:** `.env` file. **Output:** `settings` singleton used everywhere. | 30 min |
| 1.3 | **Implement database setup** | [`app/database.py`](backend-api/app/database.py) | Creates async SQLAlchemy engine + session factory. **Input:** `DATABASE_URL`. **Output:** `get_db()` dependency. | 30 min |
| 1.4 | **Implement ORM models** | [`app/models.py`](backend-api/app/models.py) | Define `Repo`, `Job`, `User` tables. **Input:** Schema definitions. **Output:** Python classes mapping to Postgres. | 1 hr |
| 1.5 | **Write initial Alembic migration** | [`alembic/versions/001_initial_schema.py`](backend-api/alembic/versions/001_initial_schema.py) | Create the 3 tables. Run `alembic upgrade head` to apply. | 1 hr |
| 1.6 | **Implement FastAPI skeleton** | [`app/main.py`](backend-api/app/main.py) | Wire up routers, CORS, middleware. **Input:** Route handlers. **Output:** Running FastAPI app at `/docs`. | 1 hr |
| 1.7 | **Implement auth middleware** | [`app/middleware/auth.py`](backend-api/app/middleware/auth.py) | Validates `X-API-Key` header on every request. Skips `/health`, `/docs`, `/webhooks`. | 30 min |
| 1.8 | **Implement schemas** | [`app/schemas.py`](backend-api/app/schemas.py) | Pydantic models for all request/response bodies. **Input:** Raw JSON. **Output:** Validated Python objects. | 1 hr |
| 1.9 | **Build mock services** | [`mocks/fake_llm_service.py`](backend-api/mocks/fake_llm_service.py), [`mocks/fake_ingestion_service.py`](backend-api/mocks/fake_ingestion_service.py) | Run on ports 8001 and 8002. **Input:** Same contract as real services. **Output:** Canned responses. **Run:** `uvicorn mocks.fake_llm_service:app --port 8001` | 1 hr |

### Phase 2: Week 2 — Core Endpoints & Celery

| # | Task | Files to Implement | What It Does | Est. Time |
|---|------|-------------------|-------------|-----------|
| 2.1 | **Implement POST /repos** | [`app/routers/repos.py`](backend-api/app/routers/repos.py) | **Input:** `{github_url, github_token}`. **Output:** `{repo_id, job_id, status}`. Creates DB records + enqueues Celery task. | 2 hrs |
| 2.2 | **Implement GET /jobs/{id}** | [`app/routers/jobs.py`](backend-api/app/routers/jobs.py) | **Input:** `job_id` (UUID). **Output:** `{status, progress, error}`. Queries DB. | 1 hr |
| 2.3 | **Set up Celery + Redis** | [`app/celery_app.py`](backend-api/app/celery_app.py) | Configure Celery app with Redis broker. **Input:** `REDIS_URL`. **Output:** Ready Celery app. | 1 hr |
| 2.4 | **Implement ingest_repo Celery task** | [`app/tasks/ingestion.py`](backend-api/app/tasks/ingestion.py) | Calls Person 2's `POST /ingest`. Updates job status in DB. **Input:** `repo_id, github_url`. **Output:** Job completed/failed. | 2 hrs |
| 2.5 | **Implement ingestion client** | [`app/services/ingestion_client.py`](backend-api/app/services/ingestion_client.py) | HTTP client for Person 2's `/ingest`, `/search`, `/delete`. **Input:** Various. **Output:** Parsed responses. | 1.5 hrs |

### Phase 3: Week 3 — Query, Webhook & RAG Logic

| # | Task | Files to Implement | What It Does | Est. Time |
|---|------|-------------------|-------------|-----------|
| 3.1 | **Implement POST /query** | [`app/routers/query.py`](backend-api/app/routers/query.py) | **Input:** `{repo_id, question, stream}`. **Output:** SSE stream of answer tokens. Calls Person 2's `/search` → assembles prompt → calls Person 1's LLM → forwards stream. | 3 hrs |
| 3.2 | **Implement LLM client** | [`app/services/llm_client.py`](backend-api/app/services/llm_client.py) | HTTP client for Person 1's `/v1/chat/completions`. Handles streaming SSE. **Input:** messages. **Output:** token stream. | 1.5 hrs |
| 3.3 | **Implement prompt builder** | [`app/services/llm_client.py`](backend-api/app/services/llm_client.py) — `build_prompt()` | Assembles token-budgeted prompt from code chunks + question. **Input:** chunks, question. **Output:** messages list. | 1 hr |
| 3.4 | **Implement webhook handler** | [`app/routers/webhooks.py`](backend-api/app/routers/webhooks.py) | Verifies HMAC signature, checks idempotency, enqueues re-ingestion. **Input:** GitHub push payload. **Output:** 200 OK. | 2 hrs |
| 3.5 | **Implement re_ingest_files task** | [`app/tasks/ingestion.py`](backend-api/app/tasks/ingestion.py) — `re_ingest_files()` | Calls Person 2's DELETE then POST for changed files. **Input:** `repo_id, file_paths`. **Output:** Updated index. | 1.5 hrs |

### Phase 4: Week 4 — Testing & Integration

| # | Task | Files to Implement | What It Does | Est. Time |
|---|------|-------------------|-------------|-----------|
| 4.1 | **Write repo/job tests** | [`tests/test_repos.py`](backend-api/tests/test_repos.py) | Test POST /repos and GET /jobs/{id} with async test client. | 1.5 hrs |
| 4.2 | **Write query tests** | [`tests/test_query.py`](backend-api/tests/test_query.py) | Test SSE streaming from POST /query. | 1 hr |
| 4.3 | **Write webhook tests** | [`tests/test_webhook.py`](backend-api/tests/test_webhook.py) | Test HMAC verification + webhook replay with captured GitHub payload. | 1.5 hrs |
| 4.4 | **Swap mocks for real services** | Update `.env` | Change `LLM_SERVICE_URL` and `INGESTION_SERVICE_URL` from mock ports to real Docker service names. | 30 min |
| 4.5 | **End-to-end test** | Manual | Walk through: `POST /repos` → poll job → `POST /query` → verify real answer. | 1 hr |
| 4.6 | **Webhook end-to-end test** | Manual | Simulate GitHub push with `smee.io` or `curl` with HMAC-signed body. Verify re-ingestion. | 1 hr |

---

## Caveats & Gotchas

### 1. **The Chunk Schema is the Most Critical Contract**
   - Person 3 builds prompt assembly logic directly against Person 2's chunk field names (`text`, `file_path`, `start_line`, `end_line`, `language`, `chunk_type`, `score`).
   - **If Person 2 changes a field name without telling you, your prompt assembly breaks silently.**
   - **Mitigation:** Write a Pydantic model (`CodeChunk` in `schemas.py`) and validate Person 2's response against it immediately.

### 2. **HMAC Verification Must Be Constant-Time**
   - Use `hmac.compare_digest()` — NOT `==` — to verify GitHub webhook signatures.
   - Using `==` opens a timing attack vulnerability.

### 3. **Webhook Idempotency is Mandatory**
   - GitHub may deliver the same webhook event multiple times.
   - Store `X-GitHub-Delivery` header values in a Redis SET with a TTL (e.g., 1 hour).
   - Return 200 for duplicates without re-processing.

### 4. **Token Budgeting for LLM Prompts**
   - Code chunks from Person 2 can exceed the LLM's context window.
   - You must truncate/rank chunks by score and fit within ~4000 tokens.
   - **Don't hardcode token counts** — use a tokenizer library or estimate by character count (~4 chars ≈ 1 token).

### 5. **Celery Task Failure Handling**
   - Network calls to Person 1 and Person 2 can fail.
   - Use `max_retries=3` with exponential backoff on Celery tasks.
   - Update the Job record with error messages so Person 4's extension can display them.

### 6. **Mock Services Must Match Contracts Exactly**
   - Your mock services (`mocks/fake_llm_service.py`, `mocks/fake_ingestion_service.py`) should return responses that match the exact field names/types of the real services.
   - Share these mocks with Person 1 and Person 2 as reference implementations.

### 7. **Rate Limiting**
   - Add `slowapi` rate limiting to `/query` endpoint to prevent abuse.
   - GitHub webhook handler should not be rate-limited (GitHub needs to reach it).

---

## Resources You'll Need

### Learning Resources (Embedded in Each Stub)

| Topic | Resource |
|-------|----------|
| **FastAPI** | [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) · [YouTube: FastAPI Full Course](https://www.youtube.com/results?search_query=fastapi+full+course+python) |
| **SQLAlchemy Async** | [SQLAlchemy Async Docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) · [YouTube: SQLAlchemy Async with FastAPI](https://www.youtube.com/results?search_query=sqlalchemy+async+fastapi+tutorial) |
| **Alembic Migrations** | [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/) · [YouTube: Alembic Tutorial](https://www.youtube.com/results?search_query=alembic+database+migrations+python) |
| **Celery** | [Celery Docs](https://docs.celeryq.dev/en/stable/) · [YouTube: Celery Python Tutorial](https://www.youtube.com/results?search_query=celery+python+tutorial+fastapi) |
| **Pydantic v2** | [Pydantic v2 Docs](https://docs.pydantic.dev/latest/) · [YouTube: Pydantic v2 Guide](https://www.youtube.com/results?search_query=pydantic+v2+tutorial+python) |
| **SSE Streaming** | [sse-starlette](https://github.com/sysid/sse-starlette) · [YouTube: FastAPI Streaming](https://www.youtube.com/results?search_query=fastapi+streaming+response+sse) |
| **RAG Pattern** | [YouTube: Build a RAG System](https://www.youtube.com/results?search_query=build+rag+system+python+fastapi) |
| **GitHub Webhooks** | [GitHub Webhook Docs](https://docs.github.com/en/webhooks) · [YouTube: Webhooks with FastAPI](https://www.youtube.com/results?search_query=github+webhooks+fastapi+python) |
| **HMAC Security** | [Python HMAC Docs](https://docs.python.org/3/library/hmac.html) · [YouTube: Webhook Security](https://www.youtube.com/results?search_query=webhook+security+hmac+verification) |
| **httpx Async** | [httpx Async Guide](https://www.python-httpx.org/async/) · [YouTube: httpx Tutorial](https://www.youtube.com/results?search_query=python+httpx+async+client+tutorial) |
| **Testing FastAPI** | [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) · [YouTube: Testing FastAPI](https://www.youtube.com/results?search_query=testing+fastapi+pytest+async) |

### Tools & Software to Install

1. **Python 3.11+** — Runtime
2. **PostgreSQL** — Primary database (install via `apt`, `brew`, or Docker)
3. **Redis** — Celery broker (install via `apt`, `brew`, or Docker)
4. **Docker** — For running Qdrant/Postgres/Redis locally during development
5. **VS Code** — Your editor (with Python, Pylance extensions)
6. **pgAdmin** or **DBeaver** — Optional: DB GUI for inspecting Postgres

### Accounts to Create

- **GitHub Account** — For testing webhooks and creating a test repo
- **Docker Hub** (optional) — For publishing the container image

### Commands You'll Run Frequently

```bash
# Start the API
uvicorn app.main:app --reload

# Start Celery worker
celery -A app.celery_app worker --loglevel=info

# Start mock services (separate terminals)
uvicorn mocks.fake_llm_service:app --port 8001
uvicorn mocks.fake_ingestion_service:app --port 8002

# Run migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description"

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=app tests/
```

---

## Repository File Map

```
backend-api/
├── .env.example              # Environment variable template
├── .gitignore
├── Dockerfile                # Container definition
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── PERSON3_PLAN.md           # ← You are here
├── alembic.ini               # Alembic configuration
├── alembic/
│   ├── env.py                # Migration environment
│   ├── script.py.mako        # Migration template
│   └── versions/
│       ├── __init__.py
│       └── 001_initial_schema.py  # STUB: First migration
├── app/
│   ├── __init__.py
│   ├── main.py               # STUB: FastAPI app entry point
│   ├── config.py             # STUB: Settings from env vars
│   ├── database.py           # STUB: Async DB engine + session
│   ├── models.py             # STUB: SQLAlchemy ORM models
│   ├── schemas.py            # STUB: Pydantic request/response models
│   ├── celery_app.py         # STUB: Celery app config
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py           # STUB: API key auth middleware
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── repos.py          # STUB: POST /repos
│   │   ├── jobs.py           # STUB: GET /jobs/{id}
│   │   ├── query.py          # STUB: POST /query (SSE streaming)
│   │   └── webhooks.py       # STUB: POST /webhooks/github
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_client.py     # STUB: HTTP client for Person 1
│   │   └── ingestion_client.py # STUB: HTTP client for Person 2
│   └── tasks/
│       ├── __init__.py
│       └── ingestion.py      # STUB: Celery tasks for ingestion
├── mocks/
│   ├── __init__.py
│   ├── fake_llm_service.py   # Mock Person 1's service
│   └── fake_ingestion_service.py # Mock Person 2's service
└── tests/
    ├── __init__.py
    ├── test_repos.py         # STUB: Repo/job endpoint tests
    ├── test_query.py         # STUB: Query endpoint tests
    └── test_webhook.py       # STUB: Webhook endpoint tests
```

---

## Dependency Map (What You Need From Others)

| You Need From | What | When | Mockable? |
|--------------|------|------|-----------|
| **Person 1** | `/v1/chat/completions` endpoint | Week 3 | ✅ Yes — `mocks/fake_llm_service.py` |
| **Person 2** | `/search`, `/ingest`, `/delete` endpoints + chunk schema | Week 2 | ✅ Yes — `mocks/fake_ingestion_service.py` |
| **Person 4** | Docker network name, container port | Day 1 | ❌ Must be agreed upfront |

## What Others Need From You

| Who | What | When |
|-----|------|------|
| **Person 4** | Working `/query` SSE endpoint + `/docs` OpenAPI spec | Week 3–4 |
| **Person 1 & 2** | Your mock services (as reference) | Week 1 |
