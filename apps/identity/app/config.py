from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    identity_database_url: str = "postgresql+psycopg://localhost:5432/identity_db"


settings = Settings()
