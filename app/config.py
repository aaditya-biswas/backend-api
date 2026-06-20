"""
Application configuration via environment variables.

RESOURCES TO LEARN:
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- FastAPI Settings & Environment Variables: https://fastapi.tiangolo.com/advanced/settings/
- YouTube: "FastAPI Settings Management with Pydantic" - https://www.youtube.com/results?search_query=fastapi+pydantic+settings+environment+variables
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/backend_api"

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # External Service URLs
    LLM_SERVICE_URL: str = "http://localhost:8001"
    INGESTION_SERVICE_URL: str = "http://localhost:8002"

    # Auth
    API_KEY: str = "dev-key"
    SECRET_KEY: str = "change-me-to-a-random-secret"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
