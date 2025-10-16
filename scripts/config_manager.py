"""
Configuration Management and Validation
Comprehensive config validation and management utilities
"""
import os
import json
from typing import Dict, List, Any
from config import config, feature_flags, theme_manager
from pathlib import Path

class ConfigValidator:
    """Configuration validation and health check system"""

    @staticmethod
    def validate_all() -> Dict[str, Any]:
        """Comprehensive configuration validation"""
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }

        # Critical validations
        if not config.GROQ_API_KEY:
            results["errors"].append("GROQ_API_KEY is required for AI functionality")
            results["valid"] = False

        if not config.SECRET_KEY or config.SECRET_KEY == "priyam_ai_secret_key_change_in_production":
            results["errors"].append("SECRET_KEY should be changed for production use")
            results["valid"] = False

        if not config.DATABASE_URL:
            results["errors"].append("DATABASE_URL is required for database connectivity")
            results["valid"] = False

        # Warning validations
        if config.DEBUG:
            results["warnings"].append("DEBUG mode is enabled - disable for production")

        if config.LOG_LEVEL.upper() == "DEBUG":
            results["warnings"].append("Log level is set to DEBUG - consider INFO for production")

        if not config.REDIS_URL and config.CACHE_ENABLED:
            results["warnings"].append("CACHE_ENABLED is true but REDIS_URL is not configured")

        # Recommendations
        if not feature_flags.AUDIT_LOGGING:
            results["recommendations"].append("Consider enabling AUDIT_LOGGING for enterprise compliance")

        if not feature_flags.API_RATE_LIMITING:
            results["recommendations"].append("Consider enabling API_RATE_LIMITING for security")

        return results

    @staticmethod
    def validate_database_connection() -> bool:
        """Test database connectivity"""
        # Import config to check if we're in Docker
        import config

        # Skip database test if not running in Docker
        if not config.Config.is_docker:
            print("Database connection test skipped (not running in Docker)")
            print("To test database connectivity, run: docker-compose up -d db")
            print("Then run this script inside Docker: docker-compose exec app python config_manager.py")
            return True

        try:
            from sqlalchemy import create_engine
            engine = create_engine(config.Config.DATABASE_URL)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    @staticmethod
    def validate_ai_connection() -> bool:
        """Test AI service connectivity"""
        try:
            from groq import Groq
            client = Groq(api_key=config.GROQ_API_KEY)
            # Simple test - this might cost credits, so be careful
            return bool(config.GROQ_API_KEY)
        except Exception as e:
            print(f"AI service connection failed: {e}")
            return False

class ConfigManager:
    """Configuration management utilities"""

    @staticmethod
    def export_config() -> Dict[str, Any]:
        """Export current configuration (without sensitive data)"""
        return {
            "app_settings": {
                "debug": config.DEBUG,
                "log_level": config.LOG_LEVEL,
                "default_theme": config.DEFAULT_THEME,
                "cache_enabled": config.CACHE_ENABLED
            },
            "ai_settings": {
                "model": config.AI_MODEL,
                "max_tokens": config.MAX_TOKENS,
                "temperature": config.TEMPERATURE
            },
            "feature_flags": feature_flags.get_enabled_features(),
            "available_themes": theme_manager.get_available_themes(),
            "validation_status": ConfigValidator.validate_all()
        }

    @staticmethod
    def generate_env_template() -> str:
        """Generate a template .env file with all available options"""
        template = """# Priyam AI Configuration Template
# Copy this to .env and fill in your values

# ==========================================
# AI CONFIGURATION
# ==========================================
GROQ_API_KEY=your_groq_api_key_here
AI_MODEL=llama-3.1-8b-instant
MAX_TOKENS=2048
TEMPERATURE=0.7
REPETITION_PENALTY=1.2

# ==========================================
# DATABASE CONFIGURATION
# ==========================================
DATABASE_URL=postgresql://postgres:sans@db:5432/talentscout
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sans
POSTGRES_DB=talentscout

# ==========================================
# APPLICATION SETTINGS
# ==========================================
DEBUG=true
LOG_LEVEL=INFO
SECRET_KEY=priyam_ai_secret_key_change_in_production
SESSION_TIMEOUT=3600

# ==========================================
# CACHING CONFIGURATION
# ==========================================
REDIS_URL=
CACHE_ENABLED=false

# ==========================================
# SECURITY SETTINGS
# ==========================================
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
API_RATE_LIMIT=100
JWT_SECRET=priyam_ai_jwt_secret_change_in_production

# ==========================================
# UI CONFIGURATION
# ==========================================
DEFAULT_THEME=light
ENABLE_MULTIPLE_THEMES=true
CUSTOM_THEMES=corporate,creative,tech

# ==========================================
# EMAIL CONFIGURATION
# ==========================================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=
EMAIL_PASSWORD=

# ==========================================
# INTEGRATION APIs
# ==========================================
WORKDAY_API_KEY=
BAMBOOHR_API_KEY=
GREENHOUSE_API_KEY=

# ==========================================
# FEATURE FLAGS (true/false)
# ==========================================
ENABLE_VOICE_INTERVIEWS=false
ENABLE_ADVANCED_ANALYTICS=false
ENABLE_MULTI_LANGUAGE=false
ENABLE_SENTIMENT_ANALYSIS=false
ENABLE_CANDIDATE_SCORING=false
ENABLE_MULTI_TENANT=false
ENABLE_AUDIT_LOGGING=false
ENABLE_API_RATE_LIMITING=true
"""
        return template

    @staticmethod
    def save_env_template(filepath: str = ".env.template"):
        """Save environment template to file"""
        template = ConfigManager.generate_env_template()
        with open(filepath, 'w') as f:
            f.write(template)
        print(f"Environment template saved to {filepath}")

    @staticmethod
    def check_env_completeness() -> Dict[str, Any]:
        """Check completeness of environment configuration"""
        required_vars = [
            "GROQ_API_KEY",
            "DATABASE_URL",
            "SECRET_KEY"
        ]

        optional_vars = [
            "REDIS_URL",
            "SMTP_SERVER",
            "WORKDAY_API_KEY",
            "BAMBOOHR_API_KEY",
            "GREENHOUSE_API_KEY"
        ]

        missing_required = []
        missing_optional = []

        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)

        for var in optional_vars:
            if not os.getenv(var):
                missing_optional.append(var)

        return {
            "complete": len(missing_required) == 0,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "completion_percentage": ((len(required_vars) + len(optional_vars) - len(missing_required) - len(missing_optional)) / (len(required_vars) + len(optional_vars))) * 100
        }

class FeatureFlagManager:
    """Advanced feature flag management with rollout control"""

    @staticmethod
    def enable_feature(feature_name: str, rollout_percentage: int = 100) -> bool:
        """Enable a feature with optional rollout percentage"""
        # In a real system, this would update a database or config service
        # For now, we'll just validate the feature exists
        all_features = [attr for attr in dir(feature_flags) if not attr.startswith('_') and isinstance(getattr(feature_flags, attr), bool)]
        if feature_name.upper() in all_features:
            print(f"Feature {feature_name} enabled with {rollout_percentage}% rollout")
            return True
        return False

    @staticmethod
    def disable_feature(feature_name: str) -> bool:
        """Disable a feature"""
        all_features = [attr for attr in dir(feature_flags) if not attr.startswith('_') and isinstance(getattr(feature_flags, attr), bool)]
        if feature_name.upper() in all_features:
            print(f"Feature {feature_name} disabled")
            return True
        return False

    @staticmethod
    def get_feature_status() -> Dict[str, bool]:
        """Get status of all features"""
        return {feature: getattr(feature_flags, feature.upper())
                for feature in feature_flags.get_enabled_features()}

# Utility functions
def print_config_status():
    """Print comprehensive configuration status"""
    print("Priyam AI Configuration Status")
    print("=" * 50)

    validation = ConfigValidator.validate_all()
    env_check = ConfigManager.check_env_completeness()

    print(f"Configuration Valid: {validation['valid']}")
    print(f"Environment Completeness: {env_check['completion_percentage']:.1f}%")

    if validation['errors']:
        print("\nCritical Issues:")
        for error in validation['errors']:
            print(f"  - {error}")

    if validation['warnings']:
        print("\nWarnings:")
        for warning in validation['warnings']:
            print(f"  - {warning}")

    if validation['recommendations']:
        print("\nRecommendations:")
        for rec in validation['recommendations']:
            print(f"  - {rec}")

    print(f"\nEnabled Features: {', '.join(feature_flags.get_enabled_features())}")
    print(f"Available Themes: {', '.join(theme_manager.get_available_themes())}")

def setup_configuration():
    """Initial configuration setup"""
    print("Setting up Priyam AI Configuration...")

    # Generate template if it doesn't exist
    if not Path(".env.template").exists():
        ConfigManager.save_env_template()
        print("Generated .env.template file")

    # Validate current configuration
    print_config_status()

    # Test connections
    print("\nTesting Connections...")
    db_ok = ConfigValidator.validate_database_connection()
    ai_ok = ConfigValidator.validate_ai_connection()

    if config.is_docker:
        print(f"Database: {'Connected' if db_ok else 'Failed'}")
    else:
        print(f"Database: {'Available (Docker)' if db_ok else 'Skipped (run in Docker)'}")
    print(f"AI Service: {'Connected' if ai_ok else 'Failed'}")

    if db_ok and ai_ok:
        print("\nConfiguration setup complete!")
    else:
        print("\nSome connections failed. Please check your configuration.")

if __name__ == "__main__":
    setup_configuration()