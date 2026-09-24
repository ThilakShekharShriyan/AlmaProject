from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    documents_database_url: str = "postgresql+psycopg://localhost:5432/documents_db"
    jwt_secret: str = "change-me-in-env-to-a-long-random-string"
    upload_dir: str = "uploads"
    max_upload_bytes: int = 10 * 1024 * 1024


settings = Settings()
