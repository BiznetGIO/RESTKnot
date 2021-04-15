import os
import logging
import json
import sys

from confluent_kafka import Consumer, KafkaException

from dnsagent.libs import knot as knot_lib


def consume():
    brokers = os.environ.get("RESTKNOT_KAFKA_BROKERS")
    topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
    agent_type = os.environ.get("RESTKNOT_AGENT_TYPE")

    conf = {
        "bootstrap.servers": brokers,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
    }
    consumer = Consumer(conf)
    consumer.suscribe(topic)

    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message.error():
                raise KafkaException(message.error())

            message = message.value()
            message = json.loads(message.decode("utf-8"))

            agent_type_msg = message["agent"]["agent_type"]
            if agent_type in agent_type_msg:

                knot_queries = message["knot"]
                for query in knot_queries:
                    knot_lib.execute(query)

    except KeyboardInterrupt:
        print("Stopping dnsagent. Press Ctrl+C again to exit")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def configure_logger():
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_format = logging.Formatter(
        "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    )
    stdout_handler.setFormatter(stdout_format)
    stdout_handler.setLevel(logging.INFO)

    root = logging.getLogger()
    root.addHandler(stdout_handler)
    root.setLevel(logging.DEBUG)


def main():
    configure_logger()
    consume()


if __name__ == "__main__":
    main()
