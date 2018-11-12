import pytest
from app import create_app
from flask import Flask
from flask_influxdb import InfluxDB


@pytest.fixture
def app():
    app = create_app()
    return app




