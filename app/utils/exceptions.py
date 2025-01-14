"""
Defines custom exceptions and registers global error handlers.
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException


class NotFoundError(Exception):
    """
    Custom exception for when a resource is not found.
    """
    pass


def register_error_handlers(app):
    """
    Registers global error handlers for the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(e):
        """
        Handles NotFoundError by returning a 404 JSON response.
        """
        return jsonify({"message": str(e)}), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """
        Handles generic HTTP exceptions (e.g., 400, 401).
        """
        return jsonify({"message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        """
        Handles any uncaught exceptions by returning a 500 JSON response.
        """
        # You can log e for debugging if needed
        return jsonify({"message": "Internal server error"}), 500
