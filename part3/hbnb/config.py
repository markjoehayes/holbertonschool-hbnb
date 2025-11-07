import os
from datetime import timedelta


class Config:
    """base configuration class - settings common to all env"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    BYCRYPT_LOG_ROUNDS = 12

    # Database settings (override in subclasses)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hbnb_dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API settings
    API_TITLE = "HBnB API"
    API_VERSION = "1.0"

    # Security settings
    JWI_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16MB max file size
    UPLOAD_FOLDER = 'app/static/uploads'


class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    TESTING = False

    # Developemnt database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hbnb_dev.db')

    # Developement specific settings
    EXPLAIN_TEMPLATE_LOADING = False

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True

    # Test database
    SQALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///hbnb_test.d')

    # Testing-specific settings/ disable CSRF for testing
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production Environment configuration"""

    def __init__(self):
        # Only check when the class is actually used

        self.DEBUG = False
        self.TESTING = False

        # Production database - MUST be set vial env variable
        self.SQALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

        if not self.SQALCHEMY_DATABASE_URI:
            raise ValueError("DATABASE_URL environment variable is required for production!")

        # Production Security settings
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required for production!")

        # call parent constructor to set other attributes
        super().__init__()
