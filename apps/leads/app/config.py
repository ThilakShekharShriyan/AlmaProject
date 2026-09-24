from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    leads_database_url: str = "postgresql+psycopg://localhost:5432/leads_db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me-in-env-to-a-long-random-string"
    lead_event_key: str = "lead_submitted"


settings = Settings()
