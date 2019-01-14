import os
import requests
from dotenv import load_dotenv
from libs import config as app
from libs import utils as util

DUMP_FOLDER = os.path.expanduser("~")


def signin(obj):
    json_data = {"username" : obj['--username'], "password" : obj['--pwd']}
    url = util.get_url('signin')
    try :
        respons = requests.post(url,json_data)
        respons = respons.json()
    except Exception as e:
        respons = str(e)
        print(respons)
        return
    if respons["code"] != 200 :
        print(respons["message"])
    else :
        return

def generate_session(username, pwd):
    pass

def create_env_file(username, password):
    if not os.path.isdir("{}/restknot".format(DUMP_FOLDER)):
        os.mkdir("{}/restknot".format(DUMP_FOLDER))    
    try :
        env_file = open("{}/restknot/.restknot.env".format(DUMP_FOLDER),"w+")
        env_file.write("OS_USERNAME=%s\n" %username)
        env_file.write("OS_PASSWORD=%s\n" %password)
        env_file.write("LOGGED_IN= %s\n" %True)
        return True
    except Exception as e:
        util.log_err(e)
        return False

def get_env_values():
    if check_env():
        load_env_file()
        restknot_env = {}
        restknot_env['username'] = os.environ.get('OS_USERNAME')
        restknot_env['password'] = os.environ.get('OS_PASSWORD')
        restknot_env['logged_in'] = os.environ.get('LOGGED_IN')
        return restknot_env
    else:
        util.log_err("Can't find restknot.env")

def load_env_file():
    return load_dotenv("{}/restknot/.restknot.env".format(DUMP_FOLDER), override=True)

def check_env():
    return os.path.isfile("{}/restknot/.restknot.env".format(DUMP_FOLDER))