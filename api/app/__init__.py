import logging
import sys

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
    stdout_handler = logging.StreamHandler(sys.stdout)

    stdout_format = logging.Formatter(
        "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    )
    stdout_handler.setFormatter(stdout_format)
    app.logger.addHandler(stdout_handler)
