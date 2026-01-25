import os
from pathlib import Path

class Config:
    """Base configuration."""
    # Project Root (CivicResolve/)
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Database (SQLite for simplicity)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'database' / 'civicresolve.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Image Storage
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Security & CORS
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    CORS_ORIGINS = ["*"]  # Allow all for development

    @staticmethod
    def init_app(app):
        """Create necessary folders on startup."""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.BASE_DIR / 'database', exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}