from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    api_key: str
    redis_url: str = "redis://localhost:6379"
    google_api_key: Optional[str] = None
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:4173"]
    
    class Config:
        env_file = ".env"


settings = Settings()
