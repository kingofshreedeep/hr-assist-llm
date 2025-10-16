"""
sans AI Configuration Management
Enhanced configuration system with feature flags and environment variable support
"""
import os
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration management for sans AI"""

    # AI Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "llama-3.1-8b-instant")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2048"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    REPETITION_PENALTY: float = float(os.getenv("REPETITION_PENALTY", "1.2"))

    # Database Configuration
    # Auto-detect if running inside Docker or locally
    # Check multiple indicators for Docker environment
    is_docker = (
        os.path.exists("/.dockerenv") or
        os.getenv("DOCKER_CONTAINER") == "true" or
        os.path.exists("/proc/1/cgroup") and "docker" in open("/proc/1/cgroup").read()
    )
    default_db_host = "db" if is_docker else "localhost"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"postgresql://postgres:sans@{default_db_host}:5432/talentscout")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "sans")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "talentscout")

    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "sans_ai_secret_key_change_in_production")
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))

    # Caching Configuration
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "false").lower() == "true"

    # Security Settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:8501,http://localhost:3000").split(",")
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", "100"))
    JWT_SECRET: str = os.getenv("JWT_SECRET", "sans_ai_jwt_secret_change_in_production")

    # UI Configuration
    DEFAULT_THEME: str = os.getenv("DEFAULT_THEME", "light")
    ENABLE_MULTIPLE_THEMES: bool = os.getenv("ENABLE_MULTIPLE_THEMES", "true").lower() == "true"
    CUSTOM_THEMES: List[str] = os.getenv("CUSTOM_THEMES", "corporate,creative,tech").split(",")

    # Email Configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_USER: str = os.getenv("EMAIL_USER", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")

    # Integration APIs
    WORKDAY_API_KEY: str = os.getenv("WORKDAY_API_KEY", "")
    BAMBOOHR_API_KEY: str = os.getenv("BAMBOOHR_API_KEY", "")
    GREENHOUSE_API_KEY: str = os.getenv("GREENHOUSE_API_KEY", "")

class FeatureFlags:
    """Feature flag management for controlled feature rollout"""

    # Advanced Features
    VOICE_INTERVIEWS: bool = os.getenv("ENABLE_VOICE_INTERVIEWS", "false").lower() == "true"
    ADVANCED_ANALYTICS: bool = os.getenv("ENABLE_ADVANCED_ANALYTICS", "false").lower() == "true"
    MULTI_LANGUAGE: bool = os.getenv("ENABLE_MULTI_LANGUAGE", "false").lower() == "true"
    SENTIMENT_ANALYSIS: bool = os.getenv("ENABLE_SENTIMENT_ANALYSIS", "false").lower() == "true"
    CANDIDATE_SCORING: bool = os.getenv("ENABLE_CANDIDATE_SCORING", "false").lower() == "true"

    # Enterprise Features
    MULTI_TENANT: bool = os.getenv("ENABLE_MULTI_TENANT", "false").lower() == "true"
    AUDIT_LOGGING: bool = os.getenv("ENABLE_AUDIT_LOGGING", "false").lower() == "true"
    API_RATE_LIMITING: bool = os.getenv("ENABLE_API_RATE_LIMITING", "true").lower() == "true"

    @classmethod
    def get_enabled_features(cls) -> List[str]:
        """Get list of all enabled features"""
        features = []
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and isinstance(getattr(cls, attr_name), bool):
                if getattr(cls, attr_name):
                    features.append(attr_name.lower())
        return features

    @classmethod
    def is_feature_enabled(cls, feature_name: str) -> bool:
        """Check if a specific feature is enabled"""
        return getattr(cls, feature_name.upper(), False)

class ThemeManager:
    """Theme management system for UI customization"""

    AVAILABLE_THEMES = {
        'corporate': {
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'accent': '#1e40af',
            'background': '#ffffff',
            'surface': '#f8fafc'
        },
        'creative': {
            'primary': '#8b5cf6',
            'secondary': '#ec4899',
            'accent': '#7c3aed',
            'background': '#ffffff',
            'surface': '#fdf2f8'
        },
        'tech': {
            'primary': '#10b981',
            'secondary': '#374151',
            'accent': '#059669',
            'background': '#ffffff',
            'surface': '#f3f4f6'
        }
    }

    @classmethod
    def get_theme_colors(cls, theme_name: str) -> dict:
        """Get color palette for a specific theme"""
        return cls.AVAILABLE_THEMES.get(theme_name, cls.AVAILABLE_THEMES['corporate'])

    @classmethod
    def get_available_themes(cls) -> List[str]:
        """Get list of available theme names"""
        return list(cls.AVAILABLE_THEMES.keys())

# Global instances
config = Config()
feature_flags = FeatureFlags()
theme_manager = ThemeManager()

def validate_configuration():
    """Validate critical configuration settings"""
    errors = []

    if not config.GROQ_API_KEY:
        errors.append("GROQ_API_KEY is required for AI functionality")

    if not config.SECRET_KEY or config.SECRET_KEY == "sans_ai_secret_key_change_in_production":
        errors.append("SECRET_KEY should be changed for production use")

    if config.DEBUG and config.LOG_LEVEL.upper() == "DEBUG":
        print("WARNING: Running in DEBUG mode with DEBUG logging")

    return errors

# Validate configuration on import
validation_errors = validate_configuration()
if validation_errors:
    print("Configuration Validation Errors:")
    for error in validation_errors:
        print(f"  - {error}")

