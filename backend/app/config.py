from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application Settings
    app_name: str = "AI Finance Advisor"
    debug: bool = True
    environment: str = "development"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # API Keys
    google_gemini_api_key: str
    alpha_vantage_api_key: str = ""
    coingecko_api_key: str = ""
    
    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    # File Upload Settings
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "./data/documents"
    
    # Vector Database Settings
    embedding_model: str = "all-MiniLM-L6-v2"
    vector_db_path: str = "./data/embeddings"
    
    # Security
    secret_key: str = "your_secret_key_here_change_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.vector_db_path, exist_ok=True)
os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
