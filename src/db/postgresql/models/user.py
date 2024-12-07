from sqlalchemy import Column, DateTime, Integer, String

from db.postgresql.database import Base


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    cpf = Column(String, index=True)
    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)
