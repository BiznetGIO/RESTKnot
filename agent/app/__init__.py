from flask import Flask
from . import configs
from flask_redis import FlaskRedis
from flask_socketio import SocketIO
import os

from app.namespace.command import *
from app.namespace.login import *
from app.helpers.redissession import RedisSessionInterface


app = Flask(__name__)
redis_store = FlaskRedis()
app.config.from_object(configs.Config)
redis_store.init_app(app)
app.session_interface = RedisSessionInterface(redis=redis_store)
root_dir = os.path.dirname(os.path.abspath(__file__))
socketio = SocketIO(app, async_mode='gevent')

# adding namespace endpoint
socketio.on_namespace(CommandNamespace('/command'))
socketio.on_namespace(LoginNamespace('/command'))


