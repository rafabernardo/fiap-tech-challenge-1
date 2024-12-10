from db.postgresql.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class OrderModel(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False, index=True)  # Status
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    order_number = Column(Integer, nullable=True, unique=True, index=True)
    owner_id = Column(Integer,ForeignKey("users.id"), nullable=True, index=True)
    payment_status = Column(String, nullable=False, index=True)  # PaymentStatus
    paid_at = Column(DateTime, nullable=True)
    total_price = Column(Integer, nullable=False)

