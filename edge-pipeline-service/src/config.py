from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Edge Pipeline Service"
    debug: bool = False
    database_url: str = "sqlite:///./edge_pipeline.db"

    # For SQLite, we need special handling
    @property
    def database_connect_args(self) -> dict:
        if self.database_url.startswith("sqlite"):
            return {"check_same_thread": False}
        return {}


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
