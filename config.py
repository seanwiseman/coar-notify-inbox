from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    allowed_admin_origins: set[str] = set()
    allowed_origins: set[str] = set()
    mongo_db_uri: str = ""
    on_receive_notification_webhook_url: str = ""

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
