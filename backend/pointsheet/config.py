import os

root_dir = os.path.dirname(os.path.abspath(__file__))


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key-for-dev")
    DATABASE = os.path.join(root_dir, "instance", "point_sheets.db.sqlite")
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_EXEMPT_ROUTES = ["/api/*"]
    SQLALCHEMY_ECHO = False
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_CHECK_DEFAULT = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DEBUG = False
    DATABASE = os.path.join(root_dir, "instance", "test_db.sqlite")
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    # In production, SECRET_KEY must be set in environment variables
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Ensure we have a secret key in production
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")


# Configuration dictionary to map environment names to config classes
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
