"""Create products table

Revision ID: 235fb2e78764
Revises: 44fef50d7d68
Create Date: 2024-12-04 19:25:27.039369

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "235fb2e78764"
down_revision: Union[str, None] = "44fef50d7d68"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column(
            "id",
            sa.Integer,
            autoincrement=True,
            primary_key=True,
            nullable=False,
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("category", sa.String, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("image", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("products")
