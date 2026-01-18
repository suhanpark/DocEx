from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8080
    reload: bool = True
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # Fireworks AI Configuration
    fireworks_api_key: str
    fireworks_model: str
    fireworks_base_url: str
    
    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: List[str] = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]
    
    # Job Configuration
    job_expiration_minutes: int = 10
    poll_interval_seconds: int = 1
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
