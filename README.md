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

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your config

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload

# Start Celery worker (in another terminal)
celery -A app.celery_app worker --loglevel=info
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
