import logging

from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .db.connection import init_app as init_db
from .routes import register_routes
from .utils.errors import ApiError


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    cors_origins = app.config.get("CORS_ORIGINS", [])
    if isinstance(cors_origins, str):
        cors_origins = Config._parse_cors_origins(cors_origins)
    if cors_origins:
        CORS(
            app,
            resources={r"/api/*": {"origins": cors_origins}},
            methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type", "Authorization"]
        )

    init_db(app)
    register_routes(app)
    _register_error_handlers(app)

    return app


def _register_error_handlers(app):
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_not_found(_error):
        response = jsonify({"error": {"message": "Resource not found.", "details": {}}})
        response.status_code = 404
        return response

    @app.errorhandler(405)
    def handle_method_not_allowed(_error):
        response = jsonify({"error": {"message": "Method not allowed.", "details": {}}})
        response.status_code = 405
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logging.exception("Unhandled application error", exc_info=error)
        response = jsonify({"error": {"message": "Internal server error.", "details": {}}})
        response.status_code = 500
        return response
