import base64
from typing import List, Optional

from pydantic import field_validator
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
    SPACING_M: int = 200
    MANAGER_EMAILS: List[str] = [
        "manager_1@email.com",
        "manager_2@email.com",
        "manager_3@email.com",
        "manager_4@email.com",
        "manager_5@email.com",
        "zijie@test.com",
        "canghai@test.com",
        "yikang@test.com",
    ]

    # Terms will be loaded from .env or os.environ:
    MONGO_DSN: Optional[str] = None
    FIREBASE_CRED: Optional[str] = None
    FIREBASE_FRONTEND_CRED: Optional[str] = None

    @field_validator("FIREBASE_CRED", "FIREBASE_FRONTEND_CRED", mode="before")
    def decode_base64_if_needed(cls, v: Optional[str]) -> Optional[str]:
        """Decode base64 values if they look encoded, otherwise return as-is."""
        if not v:
            return None
        try:
            return base64.b64decode(v.encode("utf-8")).decode("utf-8")
        except Exception:
            # Fallback: assume it's already plaintext
            return v


settings = Settings()
