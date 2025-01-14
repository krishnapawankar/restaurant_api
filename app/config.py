"""
Holds configuration classes for the Restaurant Review API.
Manages environment variables and default settings.
"""

import os


class Config:
    """
    Default Flask configuration class for the application.
    Override environment variables as needed.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
                                            "DATABASE_URL",
                                            "sqlite:///restaurant.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecret_jwt_key")
    PROPAGATE_EXCEPTIONS = True

    # Rate limit default, e.g., 10 requests per minute
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "5 per minute")

    # Flask-Caching
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))
