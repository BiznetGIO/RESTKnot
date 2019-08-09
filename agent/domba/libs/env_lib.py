from domba.libs import utils
import os
import dill

APP_HOME = utils.APP_HOME

def create_env_broker(broker, port, topic, group,flag = None):
    try:
        env_file = open("{}/.domba/broker.env".format(APP_HOME), "w+")
        env_file.write("OS_BROKER=%s\n" % broker)
        env_file.write("OS_PORTS=%s\n" % port)
        env_file.write("OS_TOPIC=%s\n" % topic)
        env_file.write("OS_FLAGS=%s\n" % flag)
        env_file.write("OS_GROUP=%s\n" % group)
        env_file.close()
        return True
    except Exception as e:
        print(e)
        return False

def create_env_knot(knot_lib, knot_socket):
    try:
        env_file = open("{}/.domba/knot.env".format(APP_HOME), "w+")
        env_file.write("OS_KNOT_LIB=%s\n" % knot_lib)
        env_file.write("OS_KNOT_SOCKS=%s\n" % knot_socket)
        return True
    except Exception as e:
        return False


def dump_session(sess):
    try:
        with open('/tmp/domba.pkl', 'wb') as f:
            dill.dump(sess, f)
    except Exception:
        utils.log_err("Dump session failed")


def remove_env(stack):
    if os.path.exists(APP_HOME+"/.domba"):
        os.remove(APP_HOME+"/.domba/"+stack+".env")
    else:
        utils.log_err("No Envi Detected")




