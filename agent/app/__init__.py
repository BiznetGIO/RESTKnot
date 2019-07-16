from flask import Flask
from . import configs
from flask_cors import CORS
import os
from app.middlewares import check_on
from app.controller import api_blueprint

app = Flask(__name__)
app.config.from_object(configs.Config)

root_dir = os.path.dirname(os.path.abspath(__file__))
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_blueprint)







