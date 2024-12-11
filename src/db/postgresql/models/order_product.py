from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.postgresql.database import Base


# OrderProductModel
class OrderProductModel(Base):
    __tablename__ = "orders_products"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer)
    price = Column(Integer)

    order = relationship("OrderModel", back_populates="order_products")
    product = relationship("ProductModel", back_populates="order_products")
