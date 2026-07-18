# Backend Orchestration API

**Person 3's Service** — The public-facing API that orchestrates the entire Codebase Q&A System.

## Overview

This service is the central nervous system of the system. It:
- Accepts repo registration and user queries via HTTP
- Manages Postgres (repos, jobs, users) and Redis (Celery broker)
- Calls Person 2's Ingestion Service to index code
- Calls Person 1's LLM Service to generate answers
- Handles GitHub webhooks for automatic re-ingestion
- Streams answers back to the VS Code extension (Person 4)

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  VS Code    │────▶│  backend-api     │────▶│  Ingestion Svc   │
│  Extension  │     │  (Person 3)      │     │  (Person 2)      │
│  (Person 4) │◀────│                  │◀────│                  │
└─────────────┘     │  ┌────────────┐  │     └──────────────────┘
                    │  │  Celery    │  │
                    │  │  + Redis   │  │     ┌──────────────────┐
                    │  └────────────┘  │────▶│  LLM Service     │
                    │  ┌────────────┐  │     │  (Person 1)      │
                    │  │  Postgres  │  │◀────│                  │
                    │  └────────────┘  │     └──────────────────┘
                    └──────────────────┘
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/repos` | Register a GitHub repo for ingestion |
| GET | `/jobs/{id}` | Poll the status of an async job |
| POST | `/query` | Ask a natural-language question about a repo |
| POST | `/webhooks/github` | Receive GitHub push events for auto-reindex |

## Prerequisites

- **Docker** (for running Postgres and Redis locally)
- **Python 3.11+**
- **pip** (Python package manager)

## Quick Start

### 1. Start Postgres (Docker)

```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=backend_api \
  -p 5432:5432 \
  -d postgres:16
```

### 2. Start Redis (Docker)

```bash
docker run --name redis \
  -p 6379:6379 \
  -d redis:7
```

### 3. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file (defaults match the Docker setup above)
cp .env.example .env
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Start the API Server

```bash
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

### 6. Start Celery Worker (separate terminal)

```bash
source .venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

### 7. Start Mock Services (separate terminals, for development)

```bash
# Terminal 3: Mock LLM Service (Person 1)
uvicorn mocks.fake_llm_service:app --port 8001

# Terminal 4: Mock Ingestion Service (Person 2)
uvicorn mocks.fake_ingestion_service:app --port 8002
```

### Stopping Docker Containers

```bash
docker stop postgres redis
docker rm postgres redis   # removes containers (data lost)
# To persist data, add -v flags when creating:
# docker run --name postgres -v postgres_data:/var/lib/postgresql/data ...
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:postgres@localhost:5432/backend_api` | Postgres connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `LLM_SERVICE_URL` | `http://localhost:8001` | Person 1's LLM service URL |
| `INGESTION_SERVICE_URL` | `http://localhost:8002` | Person 2's Ingestion service URL |
| `API_KEY` | `dev-key` | API key for authentication |
| `SECRET_KEY` | `change-me` | Secret for webhook HMAC verification |

## Docs

Once running, visit `http://localhost:8000/docs` for auto-generated OpenAPI documentation.
