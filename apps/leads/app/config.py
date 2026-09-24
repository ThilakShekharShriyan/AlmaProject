from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str = "https://example.supabase.co"
    supabase_anon_key: str = ""
    redis_url: str = "redis://localhost:6379/0"
    lead_event_key: str = "lead_submitted"


settings = Settings()
