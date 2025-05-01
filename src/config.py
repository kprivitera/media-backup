import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    JWT_AUTH_TOKEN = os.getenv("JWT_AUTH_TOKEN")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "backups")
    DATABASE = {
        "dbname": os.getenv("DB_NAME"),  # No fallback, must be set in .env
        "user": os.getenv("DB_USER"),  # No fallback, must be set in .env
        "password": os.getenv("DB_PASSWORD"),  # No fallback, must be set in .env
        "host": os.getenv("DB_HOST"),  # No fallback, must be set in .env
        "port": (
            int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else None
        ),  # No fallback
    }


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
