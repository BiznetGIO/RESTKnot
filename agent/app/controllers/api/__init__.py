from .command import *
from app import socketio

socketio.on_namespace(MyCommand("/command"))