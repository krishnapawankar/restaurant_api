"""
Provides and configures caching for the Restaurant Review API using Flask-Caching.
"""

from flask_caching import Cache

from app.config import Config

#: A global Cache instance configured based on environment variables in Config.
cache = Cache(config={
    "CACHE_TYPE": Config.CACHE_TYPE,
    "CACHE_DEFAULT_TIMEOUT": Config.CACHE_DEFAULT_TIMEOUT
})
