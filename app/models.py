"""
SQLAlchemy ORM models for Postgres tables.

INPUT: SQLAlchemy schema definitions.
OUTPUT: Python classes that map to Postgres tables (repos, jobs, users).

TABLES:
  - repos: Stores registered GitHub repositories (id, owner, name, github_url, status, commit_sha)
  - jobs: Tracks async Celery job progress (id, repo_id, type, status, error)
  - users: API key holders (id, email, api_key_hash)

RESOURCES TO LEARN:
- SQLAlchemy ORM Guide: https://docs.sqlalchemy.org/en/20/orm/
- FastAPI + SQLAlchemy Models: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models
- YouTube: "SQLAlchemy ORM Tutorial" - https://www.youtube.com/results?search_query=sqlalchemy+orm+tutorial+python
- YouTube: "Database Design Patterns" - https://www.youtube.com/results?search_query=database+design+patterns+python+sqlalchemy
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Repo(Base):
    __tablename__ = "repos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    github_url = Column(String(1024), nullable=False)
    status = Column(String(50), default="pending")  # pending, ingesting, ready, error
    commit_sha = Column(String(40), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    jobs = relationship("Job", back_populates="repo")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repo_id = Column(UUID(as_uuid=True), ForeignKey("repos.id"), nullable=False)
    type = Column(String(50), nullable=False)  # ingest, re_ingest, delete
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    progress = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    repo = relationship("Repo", back_populates="jobs")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    api_key_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
