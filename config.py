from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_db_uri: str = ""
    on_receive_notification_webhook_url: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
