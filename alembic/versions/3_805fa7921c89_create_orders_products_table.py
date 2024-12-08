"""Create orders_products table

Revision ID: 805fa7921c89
Revises: de52cb6609a8
Create Date: 2024-12-07 15:35:49.341043

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "805fa7921c89"
down_revision: Union[str, None] = "de52cb6609a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the order_products table
    op.create_table(
        "order_products",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id"), nullable=False),
        sa.Column(
            "product_id", sa.Integer, sa.ForeignKey("products.id"), nullable=False
        ),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("order_products")
