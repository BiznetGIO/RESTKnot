from flask import Flask
from . import configs
from flask_redis import FlaskRedis
import os
from flask_jwt_extended import JWTManager
from app.controller import api_blueprint

app = Flask(__name__)
redis = FlaskRedis()
jwt = JWTManager()
app.config.from_object(configs.Config)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
redis.init_app(app)
jwt.init_app(app)
root_dir = os.path.dirname(os.path.abspath(__file__))
app.register_blueprint(api_blueprint)


# adding namespace endpoint



