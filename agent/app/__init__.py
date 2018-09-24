from flask import Flask
from . import configs
import os
from flask_socketio import SocketIO
from threading import Lock

root_dir = os.path.dirname(os.path.abspath(__file__))
socketio = SocketIO()
thread = None
thread_lock  = Lock()

def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    socketio.init_app(app)

    # from .controllers import api_blueprint
    # app.register_blueprint(api_blueprint)

    return socketio, app
