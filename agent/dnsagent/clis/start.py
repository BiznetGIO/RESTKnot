import os

from dnsagent.clis.base import Base
from dnsagent.libs import knot_lib
from dnsagent.libs import kafka_lib
from dnsagent.libs import utils


class Start(Base):
    """
        usage:
            start slave
            start master

        Command :

        Options:
        -h --help                             Print usage
    """

    def execute(self):
        broker_host = os.environ.get("RESTKNOT_KAFKA_BROKER")
        broker_port = os.environ.get("RESTKNOT_KAFKA_PORTS")
        broker = f"{broker_host}:{broker_port}"
        topic = os.environ.get("RESTKNOT_KAFKA_TOPIC")
        group = os.environ.get("RESTKNOT_KAFKA_GROUP")
        flag = os.environ.get("RESTKNOT_KAFKA_FLAGS")

        if (broker_host and broker_port) is None:
            utils.log_err("Can't find kafka host and port")
            return

        if self.args["slave"]:
            try:
                utils.log_info("Connecting to broker : " + broker)
                consumer = kafka_lib.get_kafka_consumer(broker, topic, group)
            except Exception as e:
                utils.log_err("Not Connecting to broker : " + broker)
                utils.log_err("Can't Connect to broker : " + broker)
                utils.log_err("Error: " + str(e))
                exit()
            try:
                for message in consumer:
                    type_command = None
                    message = message.value
                    for i in message:
                        try:
                            type_command = message[i]["type"]
                        except Exception:
                            print("Set Your Types Command")
                    if type_command == "general":
                        knot_lib.parsing_data_general(message, broker)
                    elif type_command == "cluster":
                        knot_lib.parsing_data_cluster(message, broker, flags=flag)
                    else:
                        print("Type Command Not Found")
            except KeyboardInterrupt:
                print("Exited")
            # except Exception as e:
            #     env_lib.utils.log_err(str(e))
            exit()

        if self.args["master"]:
            try:
                utils.log_info("Connecting to broker : " + broker)
                consumer = kafka_lib.get_kafka_consumer(broker, topic, group)
            except Exception as e:
                utils.log_err(f"Can't Connect to broker: {e}")
                exit()

            try:
                for message in consumer:
                    type_command = None
                    message = message.value
                    for i in message:
                        try:
                            type_command = message[i]["type"]
                        except Exception:
                            print("Set Your Command Type")
                    if type_command == "general":
                        knot_lib.parsing_data_general(message, broker)
                    elif type_command == "cluster":
                        knot_lib.parsing_data_cluster(message, broker, flags=flag)
                    else:
                        print("Command Type Not Found")
            except Exception as e:
                utils.log_err(str(e))
