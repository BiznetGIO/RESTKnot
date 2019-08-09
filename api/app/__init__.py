from . import configs
from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
from celery import Celery
from etcd import Client
from kafka import KafkaProducer
import os, json


celery = Celery(__name__,
                broker=os.environ.get("CELERY_BROKER_URL",
                                        "amqp://admin:qazwsx@127.0.0.1:5672//"),
                backend=os.environ.get("CELERY_RESULT_BACKEND",
                                        "amqp://admin:qazwsx@127.0.0.1:5672//"))

etcd_host = os.environ.get("ETCD_HOST", os.getenv("ETCD_HOST"))                                        
etcd_port = os.environ.get("ETCD_PORT", os.getenv("ETCD_PORT"))
etcd_client = Client(host=etcd_host, port=int(etcd_port))

redis_store = FlaskRedis()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


kafka_host = os.environ.get("KAFKA_HOST", os.getenv("KAFKA_HOST"))                                        
kafka_port = os.environ.get("KAFKA_PORT", os.getenv("KAFKA_PORT"))
kafka_broker = [kafka_host+":"+kafka_port]
producer = KafkaProducer(
                bootstrap_servers=kafka_broker,
                value_serializer=lambda m: json.dumps(m).encode('utf-8'))

def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    app.config['REDIS_URL'] = os.environ.get(
        "APP_REDIS_URL","redis://:@127.0.0.1:6379/0")
    
    redis_store.init_app(app)
    celery.conf.update(app.config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .controllers import api_blueprint
    from .controllers import swaggerui_blueprint

    app.register_blueprint(swaggerui_blueprint,url_prefix=os.environ.get("/api/docs","/api/docs"))

    app.register_blueprint(api_blueprint)

    return app
