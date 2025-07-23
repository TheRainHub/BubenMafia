from functools import lru_cache
from urllib.parse import urlparse, urlunparse

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Берёт DATABASE_URL и SECRET_KEY из окружения (или .env).
    """

    database_url: PostgresDsn
    secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def sync_dsn(self) -> str:
        parsed = urlparse(str(self.database_url))
        new = parsed._replace(scheme="postgresql+psycopg2")
        return urlunparse(new)

    @property
    def async_dsn(self) -> str:
        parsed = urlparse(str(self.database_url))
        new = parsed._replace(scheme="postgresql+asyncpg")
        return urlunparse(new)


@lru_cache
def get_settings() -> Settings:
    return Settings()
