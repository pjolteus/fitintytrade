from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List, Optional, Literal
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env before anything else
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # -------------------------
    # Core App Settings
    # -------------------------
    APP_NAME: str = "FitintyTrade API"
    MODE: Literal["DEV", "PROD", "DOCKER", "RAILWAY"] = "DEV"
    IS_TESTING: bool = False

    # -------------------------
    # API & CORS
    # -------------------------
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # -------------------------
    # Database
    # -------------------------
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None

    # -------------------------
    # JWT
    # -------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # -------------------------
    # Redis / Celery
    # -------------------------
    REDIS_URL: str = "redis://localhost:6379"
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    # -------------------------
    # Email (optional)
    # -------------------------
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    EMAIL_FROM: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    # -------------------------
    # Model Paths
    # -------------------------
    LSTM_MODEL_PATH: str = "models/lstm_model.pth"

    class Config:
        env_file = ".env"
        case_sensitive = True


# -------------------------
# Singleton settings getter
# -------------------------
@lru_cache()
def get_settings():
    return Settings()

