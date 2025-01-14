# app/__init__.py

import logging

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .utils.cache import cache
from .utils.limiter import limiter

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app() -> Flask:
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s '
               '%(threadName)s : %(message)s'
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    CORS(app)

    # Define the Bearer Auth model
    authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    # Create the RESTX Api
    api = Api(
        app,
        version="1.0",
        title="Restaurant Review API",
        description="API for managing restaurants and reviews with "
                    "caching & optional async endpoints",
        prefix="/api",
        doc="/api/",  # Swagger UI endpoint
        authorizations=authorizations,
        security='Bearer'
    )

    # Error handlers (optional) – see app.utils.exceptions
    from .utils.exceptions import register_error_handlers
    register_error_handlers(app)

    # Import and register namespaces
    from .api.analytics import analytics_ns
    from .api.async_endpoint import async_ns
    from .api.auth import auth_ns
    from .api.restaurants import restaurant_ns
    from .api.reviews import review_ns

    api.add_namespace(auth_ns)
    api.add_namespace(restaurant_ns)
    api.add_namespace(review_ns)
    api.add_namespace(analytics_ns)
    api.add_namespace(async_ns)

    return app
