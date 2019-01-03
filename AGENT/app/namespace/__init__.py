from flask_socketio import SocketIO
from app import app
from .command import *
from .login import *


socketio = SocketIO(app, async_mode='gevent')

socketio.on_namespace(CommandNamespace('/command'))
socketio.on_namespace(LoginNamespace('/login'))