"""Initial migration

Revision ID: 44fef50d7d68
Revises:
Create Date: 2024-11-30 20:53:54.519296

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "44fef50d7d68"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'users' table
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer,
            autoincrement=True,
            nullable=False,
            primary_key=True,
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("cpf", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )

    # Create indexes
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_name", "users", ["name"], unique=False)
    op.create_index("ix_users_cpf", "users", ["cpf"], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index("ix_users_cpf", table_name="users")
    op.drop_index("ix_users_name", table_name="users")
    op.drop_index("ix_users_id", table_name="users")

    # Drop the 'users' table
    op.drop_table("users")
