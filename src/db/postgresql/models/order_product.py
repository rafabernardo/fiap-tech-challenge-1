from sqlalchemy import Column, ForeignKey, Integer

from db.postgresql.database import Base


class OrderProductModel(Base):
    __tablename__ = "orders_products"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer, ForeignKey("orders.id"), nullable=False, index=True
    )
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False, index=True
    )
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
