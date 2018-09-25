from flask import Flask
from . import configs
from flask_socketio import SocketIO
import os

from app.namespace.command import *


app = Flask(__name__)
app.config.from_object(configs.Config)
root_dir = os.path.dirname(os.path.abspath(__file__))
socketio = SocketIO(app, async_mode='gevent')

# adding namespace endpoint
socketio.on_namespace(CommandNamespace('/command'))


