import uuid

from db.postgresql.database import Base
from sqlalchemy import UUID, Column, DateTime, String

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    # id = Column(String, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    cpf = Column(String, index=True)
    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)
