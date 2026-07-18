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
    Create initial tables: repos, jobs, users.
    """
    # Create repos table
    op.create_table(
        "repos",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("owner", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("github_url", sa.String(1024), nullable=False),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("commit_sha", sa.String(40), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )

    # Create jobs table
    op.create_table(
        "jobs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("repo_id", UUID(as_uuid=True), sa.ForeignKey("repos.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("progress", sa.Integer(), server_default=sa.text("0")),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()")),
    )

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("api_key_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    """
    Drop all tables.
    """
    op.drop_table("jobs")
    op.drop_table("repos")
    op.drop_table("users")
