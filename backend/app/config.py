import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "Renkei"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-Powered Campus Intelligence & Innovation Platform"

    # Database
    DATABASE_URL: str = "postgresql://postgres:20062006@localhost:5432/renkei"

    # Security
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Environment
    ENV: str = "development"

    class Config:
        env_file = ".env"


# Create a single settings instance
settings = Settings()