import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS

from app.controllers import api_blueprint


def create_app():
    app = Flask(__name__)
    register_extensions(app)
    register_blueprints(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    CORS(app, resources={r"/api/*": {"origins": "*"}})


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(api_blueprint)


def configure_logger(app):
    """Configure loggers."""
    log_path = os.environ.get("RESTKNOT_LOG_FILE")
    if not log_path:
        raise ValueError(f"RESTKNOT_LOG_FILE is not set")

    file_handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=3)
    file_handler.setLevel(logging.INFO)

    file_format = logging.Formatter(
        "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    )
    file_handler.setFormatter(file_format)

    app.logger.addHandler(file_handler)
