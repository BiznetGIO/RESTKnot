import json
import os

from flask import current_app
from kafka import KafkaProducer

from app.helpers import helpers


def kafka_producer():
    """Create Kafka producer."""
    config = helpers.get_config()
    try:
        brokers = config["brokers"]
    except KeyError:
        raise ValueError("Can't find brokers list in config")

    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )
    return producer


def send(message):
    """Send given message to Kafka broker."""
    producer = None
    try:
        producer = kafka_producer()
        topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
        producer.send(topic, message)
        producer.flush()
    except Exception as e:
        current_app.logger.error(f"{e}")
        raise ValueError(f"{e}")
    finally:
        if producer:
            producer.close()
