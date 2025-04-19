from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Film Öneri Sistemi"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Veritabanı ayarları
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./movie_recommender.db")
    
    # JWT ayarları
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Öneri sistemi ayarları
    MIN_RATINGS_FOR_RECOMMENDATION: int = 5
    SIMILARITY_THRESHOLD: float = 0.5
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings() 