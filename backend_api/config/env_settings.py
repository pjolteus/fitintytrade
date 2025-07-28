# config/env_settings.py

from pydantic import BaseSettings, AnyHttpUrl, EmailStr, Field
from typing import List, Optional

class Settings(BaseSettings):
    # App Mode
    MODE: str = "DEV"
    IS_TESTING: bool = False

    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Redis / Celery
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # AI Model
    LSTM_MODEL_PATH: str = "models/lstm_model.pth"

    # Email / SMTP
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    EMAIL_FROM: Optional[EmailStr] = None
    EMAIL_PASSWORD: Optional[str] = None
    ALERT_EMAIL: Optional[EmailStr] = None
    DEV_EMAIL: Optional[EmailStr] = None

    # Broker APIs
    ALPACA_API_KEY: Optional[str]
    ALPACA_SECRET_KEY: Optional[str]
    OANDA_API_KEY: Optional[str]
    OANDA_ACCOUNT_ID: Optional[str]
    FXCM_API_TOKEN: Optional[str]
    FXCM_ACCOUNT_ID: Optional[str]
    IBR_USERNAME: Optional[str]
    IBR_PASSWORD: Optional[str]
    IBR_ACCOUNT_ID: Optional[str]
    BINANCE_API_KEY: Optional[str]
    BINANCE_SECRET_KEY: Optional[str]

    class Config:
        env_file = ".env"
        case_sensitive = True

# Usage
settings = Settings()
