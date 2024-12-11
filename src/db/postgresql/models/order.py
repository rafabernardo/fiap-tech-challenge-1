from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.postgresql.database import Base


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    order_number = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    payment_status = Column(String)
    paid_at = Column(DateTime)
    total_price = Column(Integer)

    order_products = relationship("OrderProductModel", back_populates="order")
