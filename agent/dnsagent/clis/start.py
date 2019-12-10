import os

from dnsagent.clis.base import Base
from dnsagent.libs import knot as knot_lib
from dnsagent.libs import kafka as kafka_lib
from dnsagent.libs import utils


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
        group = os.environ.get("RESTKNOT_KAFKA_GROUP")

        if (broker_host and broker_port) is None:
            utils.log_err("Can't find kafka host and port")
            exit()

        try:
            utils.log_info("Connecting to broker : " + broker)
            consumer = kafka_lib.get_kafka_consumer(broker, topic, group)
            return consumer
        except Exception as e:
            utils.log_err(f"Can't Connect to broker: {e}")
            exit()

    def take_message(self, consumer):
        flag = os.environ.get("RESTKNOT_KAFKA_FLAGS")

        try:
            for message in consumer:
                message = message.value
                knot_lib.execute(message)
        except KeyboardInterrupt:
            print("Stopping dnsagent. Press Ctrl+C again to exit")

    def execute(self):
        consumer = self.connect_kafka()
        self.take_message(consumer)
