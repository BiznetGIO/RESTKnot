from domba.clis.base import Base
from domba.libs import env_lib
import os

APP_HOME = env_lib.utils.APP_HOME

class Envi(Base): 
    """
        usage:
            envi broker
            envi knot
            envi show [-E environtment]
            envi clean [-E environtment]

        Commands :
            envi                                        Parse Yo env

        Options:
        -E environment --environment=ENVIRONMENT        Select your environment Broker or KNOT
        -h --help                                       Print usage
    """
    def execute(self):
        if not env_lib.utils.check_folder(APP_HOME+"/.domba"):
            env_lib.utils.create_folder(APP_HOME+"/.domba")
        if self.args['broker']:
            if os.path.exists(APP_HOME+"/.domba/broker.env"):
                print(".domba.env environment file exists. Do You want to remove it?")
                checks = env_lib.utils.question("Choose Y/N ")
                if checks == True:
                    broker = input("Host broker: ")
                    port = input("Port Broker: ")
                    topic = input("Topic: ")
                    group = input("Group: ")
                    flags = input("Flags: ")
                    os.remove(APP_HOME+"/.domba/broker.env")
                    env_lib.create_env_broker(broker, port, topic, group, flags)
            else:
                broker = input("Host broker: ")
                port = input("Port Broker: ")
                topic = input("Topic: ")
                group = input("Group: ")
                flags = input("Flags: ")
                env_lib.create_env_broker(broker, port, topic, group, flags)
            env = env_lib.utils.get_env_values_broker()
            exit()

        if self.args['knot']:
            if os.path.exists(APP_HOME+"/.domba/knot.env"):
                print("knot.env environment file exists. Do You want to remove it?")
                checks = env_lib.utils.question("Choose Y/N ")
                if checks == True:
                    knotlib = input("Knot Lib: ")
                    socks = input("Knot Socks Path: ")
                    os.remove(APP_HOME+"/.domba/knot.env")
                    env_lib.create_env_knot(knotlib, socks)
            else:
                knotlib = input("Knot Lib: ")
                socks = input("Knot Socks Path: ")
                env_lib.create_env_knot(knotlib, socks)
            env = env_lib.utils.get_env_values_knot()
            print(env)
            exit()

        if self.args['show']:
            envi = self.args['--environment']
            if envi == "broker":
                env_broker = env_lib.utils.get_env_values_broker()
                for i in env_broker:
                    print(i+" : "+str(env_broker[i]))
                exit()
            elif envi == "knot":
                env_knot = env_lib.utils.get_env_values_knot()
                for i in env_knot:
                    print(i+" : "+str(env_knot[i]))
                exit()
            else:
                env_lib.utils.log_err("Select Your Environment Broker or KNOT")
                exit()
            exit()

        if self.args['clean']:
            envi = self.args['--environment']
            if envi == "broker":
                checks = env_lib.utils.question("Choose Y/N ")
                if checks == True:
                    try:
                        os.remove(APP_HOME+"/.domba/broker.env")
                    except Exception as e:
                        env_lib.utils.log_err(str(e))
                    else:
                        env_lib.utils.log_warn("Broker environment removed")
                exit()
            elif envi == "knot":
                checks = env_lib.utils.question("Choose Y/N ")
                if checks == True:
                    try:
                        os.remove(APP_HOME+"/.domba/knot.env")
                    except Exception as e:
                        env_lib.utils.log_err(str(e))
                    else:
                        env_lib.utils.log_warn("KNOT environment removed")
                exit()
            else:
                env_lib.utils.log_info("Remove All Environment")
                checks = env_lib.utils.question("Choose Y/N ")
                try:
                    env_lib.utils.remove_folder(APP_HOME+"/.domba")
                except Exception as e:
                    env_lib.utils.log_err(str(e))
                else:
                    env_lib.utils.log_warn("Environment Remove")
                exit()
            exit()