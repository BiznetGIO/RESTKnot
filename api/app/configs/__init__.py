import os
from celery.schedules import crontab

class Config():
    redis_uri = os.environ.get(
        "APP_REDIS_URL","redis://:@127.0.0.1:6379/0")
    celer_broker = os.environ.get(
        "CELERY_BROKER_URL","amqp://admin:@127.0.0.1:5672//")
    celery_backend = os.environ.get(
        "CELERY_RESULT_BACKEND","amqp://admin:@127.0.0.1:5672//")
    DEBUG = True
    REDIS_URL = redis_uri
    CELERY_BROKER_URL = celer_broker
    CELERY_RESULT_BACKEND = celery_backend