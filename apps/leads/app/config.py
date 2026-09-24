from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    leads_database_url: str = "postgresql+psycopg://localhost:5432/leads_db"


settings = Settings()
