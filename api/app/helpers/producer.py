import json
import os

from flask import current_app
from confluent_kafka import Producer

from app.helpers import helpers


def kafka_producer():
    """Create Kafka producer."""
    config = helpers.get_config()
    try:
        brokers = config["brokers"]
    except KeyError:
        raise ValueError("Can't find brokers list in config")

    brokers = ",".join(brokers)
    conf = {"bootstrap.servers": brokers}
    producer = Producer(**conf)
    return producer


def _delivery_report(err, msg):
    if err is not None:
        raise ValueError(f"Message delivery failed: {err}")


def send(message):
    """Send given message to Kafka broker."""
    producer = None
    try:
        producer = kafka_producer()
        topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
        encoded_message = json.dumps(message).encode("utf-8")
        producer.produce(topic, encoded_message, callback=_delivery_report)
    except Exception as e:
        current_app.logger.error(f"{e}")
        raise ValueError(f"{e}")

    # Serve delivery callback queue.
    producer.poll(0)
    # Wait until all messages have been delivered
    producer.flush()
