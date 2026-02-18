"""Application settings and environment configuration"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Application Settings
    app_name: str = "D&D API"
    environment: str = Field(default="dev")
    debug: bool = Field(default=True)

    # API Settings
    api_version: str = "v1"

    # AWS Settings (for Lambda deployment)
    aws_region: str = "us-east-1"

    # CORS Settings
    cors_allowed_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Create cached settings instance.
    Environment variables will override defaults:
    - ENVIRONMENT: dev, staging, prod
    - DEBUG: true, false
    """
    return Settings()


def get_cors_origins() -> list[str]:
    """Get CORS origins from settings as a cleaned list."""
    settings = get_settings()
    return [
        origin.strip()
        for origin in settings.cors_allowed_origins.split(",")
        if origin.strip()
    ]
