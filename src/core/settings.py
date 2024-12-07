from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_PORT: int
    ROOT_PATH: str = "/fiap-soat"

    MONGO_URI: str | None = None
    MONGO_URL: str
    MONGO_PORT: int
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str

    POSTGRESQL_URI: str | None = None
    POSTGRESQL_URL: str
    POSTGRESQL_PORT: int
    POSTGRESQL_USERNAME: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()
