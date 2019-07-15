import os
from . import configs
from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
import psycopg2
from celery import Celery

redis_store = FlaskRedis()
root_dir = os.path.dirname(os.path.abspath(__file__))

conn = psycopg2.connect(
    database=os.environ.get("DB_NAME", os.getenv('DB_NAME')),
    user=os.environ.get("DB_USER", os.getenv('DB_USER')),
    password=os.environ.get("DB_PASSWORD", os.getenv('DB_PASSWORD')),
    sslmode=os.environ.get("DB_SSL", os.getenv('DB_SSL')),
    port=os.environ.get("DB_PORT", os.getenv('DB_PORT')),
    host=os.environ.get("DB_HOST", os.getenv('DB_HOST'))
)

celery = Celery(__name__,
                broker=os.environ.get("CELERY_BROKER_URL",
                                        os.getenv("CELERY_BROKER_URL")),
                backend=os.environ.get("CELERY_RESULT_BACKEND",
                                        os.getenv("CELERY_BROKER_URL")))

conn.set_session(autocommit=True)
db = conn.cursor()

cs_storage = os.environ.get("CLUSTER_STORAGE", "database")

def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    app.config['REDIS_URL'] = os.environ.get(
        "FLASK_REDIS_URL",os.getenv("FLASK_REDIS_URL"))
    app.config['PROPAGATE_EXCEPTIONS'] = True
    redis_store.init_app(app)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .controllers import api_blueprint
    from .controllers import swaggerui_blueprint

    app.register_blueprint(swaggerui_blueprint, url_prefix=os.environ.get("SWAGGER_URL", os.getenv('SWAGGER_URL')))
    app.register_blueprint(api_blueprint)

    return app
