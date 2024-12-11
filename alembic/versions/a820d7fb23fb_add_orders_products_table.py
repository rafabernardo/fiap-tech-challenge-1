"""Add orders_products table

Revision ID: a820d7fb23fb
Revises: de52cb6609a8
Create Date: 2024-12-10 00:26:31.939008

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a820d7fb23fb"
down_revision: Union[str, None] = "de52cb6609a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders_products",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column(
            "order_id", sa.Integer, sa.ForeignKey("orders.id"), nullable=False
        ),
        sa.Column(
            "product_id",
            sa.Integer,
            sa.ForeignKey("products.id"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table("orders_products")
