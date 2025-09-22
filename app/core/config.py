from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    MONGO_DSN: str = "mongodb://localhost:27017/fastapi_db"
    FIREBASE_CRED_PATH: str | None = None  # None values will be covered by values in .env

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
