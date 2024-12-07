"""Create orders_products table

Revision ID: 805fa7921c89
Revises: de52cb6609a8
Create Date: 2024-12-07 15:35:49.341043

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

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
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # Create indexes
    op.create_index("ix_order_products_id", "order_products", ["id"])
    op.create_index("ix_order_products_order_id", "order_products", ["order_id"])
    op.create_index("ix_order_products_product_id", "order_products", ["product_id"])
    op.create_index("idx_order_product", "order_products", ["order_id", "product_id"])


def downgrade():
    # Drop indexes and table
    op.drop_index("idx_order_product", table_name="order_products")
    op.drop_index("ix_order_products_product_id", table_name="order_products")
    op.drop_index("ix_order_products_order_id", table_name="order_products")
    op.drop_index("ix_order_products_id", table_name="order_products")
    op.drop_table("order_products")
