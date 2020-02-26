import os
import json
from kafka import KafkaProducer
from flask import current_app


def kafka_producer():
    """Create Kafka producer."""
    host = os.environ.get("KAFKA_HOST")
    port = os.environ.get("KAFKA_PORT")
    broker = f"{host}:{port}"

    producer = KafkaProducer(
        bootstrap_servers=[broker],
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
