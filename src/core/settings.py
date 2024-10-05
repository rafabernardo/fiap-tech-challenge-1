from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_PORT: int
    MONGO_URL: str
    MONGO_PORT: int
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()
