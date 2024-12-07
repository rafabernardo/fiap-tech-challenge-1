from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from core.settings import get_settings

settings = get_settings()
engine = create_engine(settings.POSTGRESQL_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_postgresql_session() -> Generator[Session, None, None]:
    """
    Context manager to provide a transactional scope around operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
