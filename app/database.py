"""
Database engine and session configuration using SQLAlchemy async.

INPUT: DATABASE_URL from settings (PostgreSQL connection string).
OUTPUT: Async SQLAlchemy engine and session factory for DB operations.

RESOURCES TO LEARN:
- SQLAlchemy Async Docs: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- FastAPI + SQLAlchemy: https://fastapi.tiangolo.com/tutorial/sql-databases/
- Alembic Migrations: https://alembic.sqlalchemy.org/en/latest/
- YouTube: "SQLAlchemy Async with FastAPI" - https://www.youtube.com/results?search_query=sqlalchemy+async+fastapi+tutorial
- YouTube: "Alembic Database Migrations" - https://www.youtube.com/results?search_query=alembic+database+migrations+python
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """Dependency that provides an async database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
