from contextlib import contextmanager
from functools import lru_cache, wraps

from core.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

settings = get_settings()
engine = create_engine(settings.POSTGRESQL_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_postgresql_session() -> Session:
    """
    Context manager to provide a transactional scope around operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
