"""
Initial database schema migration.

Creates the three core tables: repos, jobs, users.

INPUT: Alembic upgrade command.
OUTPUT: Postgres tables created.

RESOURCES TO LEARN:
- Alembic Operations: https://alembic.sqlalchemy.org/en/latest/ops.html
- YouTube: "Alembic Migrations Step by Step" - https://www.youtube.com/results?search_query=alembic+migration+python+fastapi
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    STUB: Create initial tables.
    
    TODO:
    1. Create 'repos' table with columns: id (UUID PK), owner, name, github_url,
       status, commit_sha, created_at, updated_at
    2. Create 'jobs' table with columns: id (UUID PK), repo_id (FK→repos),
       type, status, progress, error, created_at, updated_at
    3. Create 'users' table with columns: id (UUID PK), email (unique),
       api_key_hash, created_at
    """
    raise NotImplementedError("Implement initial migration upgrade")


def downgrade() -> None:
    """
    STUB: Drop all tables.
    
    TODO:
    1. Drop 'jobs' table
    2. Drop 'repos' table
    3. Drop 'users' table
    """
    raise NotImplementedError("Implement initial migration downgrade")
