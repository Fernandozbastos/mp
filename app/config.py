from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "mp"
    database_url: str = "postgresql+asyncpg://user:password@localhost/db"

    class Config:
        env_file = ".env"


settings = Settings()
