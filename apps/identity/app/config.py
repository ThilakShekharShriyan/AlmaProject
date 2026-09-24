from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    identity_database_url: str = "postgresql+psycopg://localhost:5432/identity_db"
    jwt_secret: str = "change-me-in-env-to-a-long-random-string"
    jwt_ttl_hours: int = 8
    attorney_email: str = "attorney@example.com"
    attorney_password: str = "change-me"


settings = Settings()
