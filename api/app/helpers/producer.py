import os
import json
from kafka import KafkaProducer


def kafka_producer():
    host = os.environ.get("KAFKA_HOST")
    port = os.environ.get("KAFKA_PORT")
    broker = f"{host}:{port}"

    producer = KafkaProducer(
        bootstrap_servers=[broker],
        value_serializer=lambda m: json.dumps(m).encode("utf-8"),
    )
    return producer


def send(command):
    try:
        producer = kafka_producer()
        topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
        respons = producer.send(topic, command)
    except Exception as e:
        raise e
    else:
        respons.get(timeout=60)
        return respons.is_done
