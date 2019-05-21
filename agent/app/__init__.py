from flask import Flask
from . import configs
import os
from app.controller import api_blueprint

app = Flask(__name__)
app.config.from_object(configs.Config)
root_dir = os.path.dirname(os.path.abspath(__file__))
app.register_blueprint(api_blueprint)



