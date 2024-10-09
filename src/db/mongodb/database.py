from functools import lru_cache, wraps

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from core.settings import get_settings

settings = get_settings()

@lru_cache(1)
def get_mongo_client() -> MongoClient:
    if settings.MONGO_URI:
        return MongoClient(settings.MONGO_URI)

    mongo_client = MongoClient(
        host=settings.MONGO_URL,
        port=settings.MONGO_PORT,
        username=settings.MONGO_USERNAME,
        password=settings.MONGO_PASSWORD,
    )
    return mongo_client


def get_mongo_database():
    client = get_mongo_client()
    database = client[settings.MONGO_DATABASE]
    return database


def mongo_transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client = get_mongo_client()
        session = client.start_session()
        try:
            with session.start_transaction():
                result = func(*args, **kwargs, session=session)
            return result
        except PyMongoError as exc:
            session.abort_transaction()
            print(f"Transaction aborted due to error: {exc}")
            raise
        finally:
            session.end_session()

    return wrapper
