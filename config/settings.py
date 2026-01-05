"""
Settings and configuration management.
Loads from environment variables and .env file.
"""

import os
from typing import Optional
from dataclasses import dataclass, field


def _get_env(key: str, default: str = "") -> str:
    """Get environment variable with fallback to default."""
    return os.environ.get(key, default)


def _get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean environment variable."""
    value = os.environ.get(key, str(default)).lower()
    return value in ("true", "1", "yes")


@dataclass
class Settings:
    """Application settings loaded from environment."""
    
    # General
    environment: str = field(default_factory=lambda: _get_env("ENVIRONMENT", "development"))
    debug: bool = field(default_factory=lambda: _get_env_bool("DEBUG", True))
    
    # LLM Configuration
    openai_api_key: Optional[str] = field(default_factory=lambda: _get_env("OPENAI_API_KEY") or None)
    openai_model: str = field(default_factory=lambda: _get_env("OPENAI_MODEL", "gpt-4"))
    
    # Database
    database_url: Optional[str] = field(default_factory=lambda: _get_env("DATABASE_URL") or None)
    
    # Messaging
    wechat_app_id: Optional[str] = field(default_factory=lambda: _get_env("WECHAT_APP_ID") or None)
    wechat_app_secret: Optional[str] = field(default_factory=lambda: _get_env("WECHAT_APP_SECRET") or None)
    
    # Workflow
    default_thread_id: str = field(default_factory=lambda: _get_env("DEFAULT_THREAD_ID", "influencer_outreach_001"))
    max_retries: int = field(default_factory=lambda: int(_get_env("MAX_RETRIES", "3")))
    
    def __post_init__(self):
        """Load .env file if it exists."""
        self._load_dotenv()
    
    def _load_dotenv(self):
        """Try to load .env file using python-dotenv if available."""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            # Reload values after loading .env
            self.openai_api_key = _get_env("OPENAI_API_KEY") or None
            self.database_url = _get_env("DATABASE_URL") or None
            self.wechat_app_id = _get_env("WECHAT_APP_ID") or None
            self.wechat_app_secret = _get_env("WECHAT_APP_SECRET") or None
        except ImportError:
            pass  # python-dotenv not installed, skip
    
    def validate(self) -> list[str]:
        """Validate required settings. Returns list of missing/invalid settings."""
        errors = []
        
        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY is not set")
        
        return errors
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
