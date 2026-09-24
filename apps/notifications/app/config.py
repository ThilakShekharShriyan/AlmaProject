from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis_url: str = "redis://localhost:6379/0"
    lead_event_key: str = "lead_submitted"
    smtp_host: str = "127.0.0.1"
    smtp_port: int = 1025
    smtp_from: str = "leads@localhost"
    attorney_notification_email: str = "attorney@example.com"


settings = Settings()
