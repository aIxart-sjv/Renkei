from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Central configuration for Renkei backend
    Loads values from .env file automatically
    """

    # =========================
    # APP SETTINGS
    # =========================

    APP_NAME: str = "Renkei API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_PREFIX: str = "/api"


    # =========================
    # DATABASE SETTINGS
    # =========================

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "20062006"
    POSTGRES_DB: str = "renkei"

    DATABASE_URL: str | None = None


    # =========================
    # JWT AUTH SETTINGS
    # =========================

    JWT_SECRET_KEY: str = "CHANGE_THIS_SECRET"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


    # =========================
    # ML MODEL PATHS
    # =========================

    ML_MODEL_DIR: str = "app/ml/models/saved"

    EMBEDDING_MODEL_PATH: str = "app/ml/models/saved/embedder.pkl"

    RECOMMENDER_MODEL_PATH: str = "app/ml/models/saved/recommender.pkl"

    INNOVATION_MODEL_PATH: str = "app/ml/models/saved/innovation_model.pkl"


    # =========================
    # GRAPH SETTINGS
    # =========================

    GRAPH_CACHE_ENABLED: bool = True


    # =========================
    # ENV FILE CONFIG
    # =========================

    class Config:
        env_file = ".env"
        case_sensitive = True


    # =========================
    # BUILD DATABASE URL
    # =========================

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:

        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


# Cached settings instance
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Global settings object
settings = get_settings()