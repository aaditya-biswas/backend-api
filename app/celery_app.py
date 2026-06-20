"""
Celery application configuration for async task processing.

INPUT: Reads Redis URL from settings to configure Celery broker/backend.
OUTPUT: A configured Celery app instance that can register and run async tasks.

RESOURCES TO LEARN:
- Celery Official Docs: https://docs.celeryq.dev/en/stable/
- Celery with FastAPI: https://fastapi.tiangolo.com/how-to/celery/
- YouTube: "Celery Python Tutorial" - https://www.youtube.com/results?search_query=celery+python+tutorial+fastapi
- YouTube: "Async Tasks with Celery and Redis" - https://www.youtube.com/results?search_query=celery+redis+async+tasks+python
"""

from celery import Celery

from app.config import settings

celery_app = Celery(
    "backend_api",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
