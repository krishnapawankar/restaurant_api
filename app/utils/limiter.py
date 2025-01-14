"""
Configures Flask-Limiter for request rate limiting.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.config import Config

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Config.RATELIMIT_DEFAULT],  # e.g. "10 per minute"
)
