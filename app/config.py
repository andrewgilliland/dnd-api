import os
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    # Application Settings
    app_name: str = "D&D API"
    environment: str = "dev"
    debug: bool = True

    # API Settings
    api_version: str = "v1"

    # AWS Settings (for Lambda deployment)
    aws_region: str = "us-east-1"

    class Config:
        case_sensitive = False

    def __init__(self, **kwargs):
        # Override with environment variables
        env = os.getenv("ENVIRONMENT", "dev")
        print(f"Loading settings for environment: {env}")
        debug = os.getenv("DEBUG", "true").lower() == "true"

        super().__init__(environment=env, debug=debug, **kwargs)


@lru_cache()
def get_settings() -> Settings:
    """
    Create cached settings instance.
    Environment variables will override defaults:
    - ENVIRONMENT: dev, staging, prod
    - DEBUG: true, false
    """
    return Settings()


settings = get_settings()
