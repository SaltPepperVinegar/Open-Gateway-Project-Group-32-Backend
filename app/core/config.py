from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    APP_NAME: str = "Disaster Rescue API"
    APP_NAME_TEST: str = "Disaster Rescue API (Test)"
    DB_NAME: str = "opgw"
    DB_NAME_TEST: str = "opgw_test"
    
    MANAGER_EMAILS: List[str] = ["manager_1@email.com", "manager_2@email.com"]

    # Terms will be loaded from .env or os.environ:
    MONGO_DSN: str | None = None
    FIREBASE_CRED_PATH: str | None = None


settings = Settings()
