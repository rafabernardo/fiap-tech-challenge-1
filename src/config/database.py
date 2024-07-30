from functools import wraps

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config.settings import get_settings

settings = get_settings()

client = MongoClient(
    host=settings.MONGO_URL,
    port=settings.MONGO_PORT,
    username=settings.MONGO_USERNAME,
    password=settings.MONGO_PASSWORD,
)


def get_mongo_database():
    database = client[settings.MONGO_DATABASE]
    return database


def mongo_transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = client.start_session()
        try:
            with session.start_transaction():
                result = func(*args, **kwargs, session=session)
            return result
        except PyMongoError as e:
            session.abort_transaction()
            print(f"Transaction aborted due to error: {e}")
            raise
        finally:
            session.end_session()

    return wrapper
