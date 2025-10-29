"""
Configuration management.
Handles API keys and settings from environment variables or .env file.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Application configuration."""

    def __init__(self):
        self.api_key: Optional[str] = None
        self.model: str = "gemini-2.5-pro"
        self.debug: bool = False

    @classmethod
    def load(cls) -> 'Config':
        """
        Load configuration from environment.

        Checks (in order):
        1. Environment variables
        2. .env file in current directory
        3. .env file in home directory
        """
        # Load .env file if exists
        env_paths = [
            Path('.env'),
            Path.home() / '.gitstory' / '.env'
        ]

        for path in env_paths:
            if path.exists():
                load_dotenv(path)
                break

        config = cls()
        config.api_key = os.getenv('GITSTORY_API_KEY')
        config.model = os.getenv('GITSTORY_MODEL', 'gemini-2.5-pro')
        config.debug = os.getenv('DEBUG', '').lower() in ('1', 'true', 'yes')

        return config

    def validate(self) -> bool:
        """Validate configuration."""
        return self.api_key is not None and len(self.api_key) > 0
