from dnsagent.clis.base import Base
from dnsagent.libs import env_lib
from dnsagent.libs import knot_lib
from dnsagent.libs import kafka_lib


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
        # knot_lib.utils.check_root()
        broker_env = env_lib.utils.get_env_values_broker()
        broker = broker_env["broker"] + ":" + broker_env["port"]
        topic = broker_env["topic"]
        group = broker_env["group"]
        flag = broker_env["flags"]

        if self.args["slave"]:
            try:
                knot_lib.utils.log_err("Connecting to broker : " + broker)
                consumer = kafka_lib.get_kafka_consumer(broker, topic, group)
            except Exception as e:
                knot_lib.utils.log_err("Not Connecting to broker : " + broker)
                knot_lib.utils.log_err("Error: " + str(e))
                exit()
            try:
                for message in consumer:
                    type_command = None
                    message = message.value
                    for i in message:
                        try:
                            type_command = message[i]["type"]
                        except Exception as e:
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
                knot_lib.utils.log_err("Connecting to broker : " + broker)
                consumer = kafka_lib.get_kafka_consumer(broker, topic, group)
            except Exception as e:
                knot_lib.utils.log_err("Not Connecting to broker : " + broker)
                knot_lib.utils.log_err("Error: " + str(e))
                exit()
            try:
                for message in consumer:
                    type_command = None
                    message = message.value
                    for i in message:
                        try:
                            type_command = message[i]["type"]
                        except Exception as e:
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
