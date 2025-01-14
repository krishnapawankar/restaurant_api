# app/utils/exceptions.py
from flask import jsonify
from werkzeug.exceptions import HTTPException


class NotFoundError(Exception):
    """Resource not found exception."""
    pass


def register_error_handlers(app):
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(e):
        return jsonify({"message": str(e)}), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        # You can log e for debugging if needed
        return jsonify({"message": "Internal server error"}), 500
