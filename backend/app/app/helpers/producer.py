from typing import Any, Callable, Collection, Dict

import json
import logging
import os
from functools import wraps

from confluent_kafka import Producer
from fastapi import HTTPException

from app.helpers import helpers


def kafka_producer() -> Producer:
    """Create Kafka producer."""
    config = helpers.get_config()
    try:
        brokers = config["brokers"]
    except KeyError:
        raise ValueError("failed to find brokers list in the configuration file")

    brokers = ",".join(brokers)
    conf = {"bootstrap.servers": brokers}
    producer = Producer(**conf)
    return producer


def check_producer(f: Callable) -> Callable:
    """Check producer availability"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            kafka_producer()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"{e}",
            )
        else:
            return f(*args, **kwargs)

    return decorated_function


def _delivery_report(err: str, _: Any = None):
    """
    :param Any _: To make it compatible with `produce` callback.
    """
    if err is not None:
        raise ValueError(f"message delivery failed: {err}")


def send(message: Dict[str, Collection[Collection[str]]]):
    """Send given message to Kafka broker."""
    producer = None
    try:
        producer = kafka_producer()
        topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
        encoded_message = json.dumps(message).encode("utf-8")
        producer.produce(topic, encoded_message, callback=_delivery_report)
    except Exception as e:
        logging.error("%s", e)
        raise ValueError(f"{e}")

    # Serve delivery callback queue.
    producer.poll(0)
    # Wait until all messages have been delivered
    producer.flush()
