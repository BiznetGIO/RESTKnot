import os
from . import configs
from flask import Flask
from werkzeug.contrib.cache import MemcachedCache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis
from socketIO_client import SocketIO, BaseNamespace
import psycopg2

redis_store = FlaskRedis()
cache = MemcachedCache(['{}:{}'.format(os.getenv('MEMCACHE_HOST'), os.getenv('MEMCACHE_PORT'))])
sockets = SocketIO(os.getenv('SOCKET_AGENT_HOST'), os.getenv('SOCKET_AGENT_PORT'))
jwt = JWTManager()
root_dir = os.path.dirname(os.path.abspath(__file__))
conn = psycopg2.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    sslmode=os.getenv('DB_SSL'),
    port=os.getenv('DB_PORT'),
    host=os.getenv('DB_HOST')
)

conn.set_session(autocommit=True)
db = conn.cursor()

def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    redis_store.init_app(app)
    jwt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .controllers import api_blueprint
    from .controllers import swaggerui_blueprint

    app.register_blueprint(swaggerui_blueprint, url_prefix=os.getenv('SWAGGER_URL'))
    app.register_blueprint(api_blueprint)

    return app
