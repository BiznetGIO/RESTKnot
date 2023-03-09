import json
import logging
import os
import sys
import time

from confluent_kafka import Consumer, KafkaException

from dnsagent import agent

logger = logging.getLogger(__name__)


def main():
    configure_logger()
    consume()


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


def consume():
    brokers = os.environ.get("RESTKNOT_KAFKA_BROKERS")
    topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
    group_id = os.environ.get("RESTKNOT_KAFKA_GROUP_ID")
    agent_type = os.environ.get("RESTKNOT_AGENT_TYPE")
    command_delay = int(os.environ.get("RESTKNOT_COMMAND_DELAY", 5))

    conf = {
        "bootstrap.servers": brokers,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
    }

    def print_assignment(consumer, partitions):
        logger.info(f"Consumer assigned to: {partitions}")

    consumer = Consumer(conf)
    consumer.subscribe([topic], on_assign=print_assignment)

    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                raise KafkaException(message.error())

            message = message.value()
            message = json.loads(message.decode("utf-8"))

            agent_type_msg = message["agent"]["agent_type"]
            if agent_type in agent_type_msg:
                knot_queries = message["knot"]
                for query in knot_queries:
                    print(f"Delaying next command by {command_delay} seconds...")
                    time.sleep(command_delay)
                    agent.execute(query)

    except KeyboardInterrupt:
        print(" dnsagent stopped. Aborted by user")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
