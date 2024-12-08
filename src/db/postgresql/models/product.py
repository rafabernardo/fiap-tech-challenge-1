import uuid

from sqlalchemy import Column, DateTime, Integer, String

from db.postgresql.database import Base


class ProductModel(Base):
    __tablename__ = "products"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
