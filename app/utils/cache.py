# app/utils/cache.py
from flask_caching import Cache

from app.config import Config

cache = Cache(config={
    "CACHE_TYPE": Config.CACHE_TYPE,
    "CACHE_DEFAULT_TIMEOUT": Config.CACHE_DEFAULT_TIMEOUT
})
