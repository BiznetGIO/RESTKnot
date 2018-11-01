from flask import Flask
from celery import Celery
from flask_redis import FlaskRedis
from influxdb import InfluxDBClient
from flask_cors import CORS
from socketIO_client import SocketIO, BaseNamespace
from . import configs
import os

redis_store = FlaskRedis()
influx = InfluxDBClient(host=os.getenv('INFLUXDB_HOST'), port=os.getenv('INFLUXDB_PORT'))
celery = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))
root_dir = os.path.dirname(os.path.abspath(__file__))

sockets = SocketIO(os.getenv('SOCKET_AGENT_HOST'), os.getenv('SOCKET_AGENT_PORT'))


def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    redis_store.init_app(app)
    celery.conf.update(app.config)
    # socket.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .controllers import api_blueprint

    app.register_blueprint(api_blueprint)

    return app
