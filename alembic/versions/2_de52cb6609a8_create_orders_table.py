"""Create orders table

Revision ID: de52cb6609a8
Revises: 235fb2e78764
Create Date: 2024-12-07 15:21:02.249642

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "de52cb6609a8"
down_revision: Union[str, None] = "235fb2e78764"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create orders table
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=True),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("order_number", sa.Integer, nullable=True, unique=True),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("payment_status", sa.String, nullable=False),
        sa.Column("paid_at", sa.DateTime, nullable=True),
        sa.Column("total_price", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("orders")
