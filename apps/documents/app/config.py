from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    supabase_url: str = "https://example.supabase.co"
    supabase_anon_key: str = ""
    max_upload_bytes: int = 10 * 1024 * 1024


settings = Settings()
