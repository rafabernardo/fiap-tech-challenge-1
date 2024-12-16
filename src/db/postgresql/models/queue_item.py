from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from db.postgresql.database import Base


class QueueItemModel(Base):
    __tablename__ = "queue_items"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, autoincrement=True, primary_key=True)
    order_id: str
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    orders = relationship(
        "OrderModel",
        back_populates="order",
    )
