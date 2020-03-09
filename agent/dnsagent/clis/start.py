import os
import logging

from dnsagent.clis.base import Base
from dnsagent.libs import kafka as kafka_lib
from dnsagent.libs import knot as knot_lib


logger = logging.getLogger(__name__)


class Start(Base):
    """
        usage:
            start

        Command :

        Options:
        -h --help                             Print usage
    """

    def connect_kafka(self):
        broker_host = os.environ.get("RESTKNOT_KAFKA_BROKER")
        broker_port = os.environ.get("RESTKNOT_KAFKA_PORTS")
        broker = f"{broker_host}:{broker_port}"
        topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")

        if (broker_host and broker_port) is None:
            logger.info("Can't find kafka host and port")
            exit()

        try:
            logger.info("Connecting to broker : " + broker)
            consumer = kafka_lib.get_kafka_consumer(broker, topic)
            return consumer
        except Exception as e:
            logger.info(f"Can't Connect to broker: {e}")
            exit()

    def take_message(self, consumer):
        agent_type = os.environ.get("RESTKNOT_AGENT_TYPE")

        try:
            for message in consumer:
                message = message.value

                agent_type_msg = message["agent"]["agent_type"]
                if agent_type in agent_type_msg:

                    knot_queries = message["knot"]
                    for query in knot_queries:
                        knot_lib.execute(query)

            consumer.close()

        except KeyboardInterrupt:
            print("Stopping dnsagent. Press Ctrl+C again to exit")

    def execute(self):
        consumer = self.connect_kafka()
        self.take_message(consumer)
