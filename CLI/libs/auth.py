from __future__ import unicode_literals
from prompt_toolkit.shortcuts import confirm

import getpass
import sys
import os
import requests
import dill
from dotenv import load_dotenv
from libs import utils as util
import subprocess as sp
import time
from cmd import Cmd
import json
import datetime

DUMP_FOLDER = os.path.expanduser("~")

def get_username(): #pragma: no cover
    usr = input("username : ")
    usr = str(usr)
    return usr

def get_password():
    return getpass.getpass("password : ")


def send_todb(user_id,project_id) : 
    data = {"project_id" : project_id , "user_id" : user_id}
    headers = {'Content-Type': "application/json"}
    try :
        url = util.get_url('user')
        requests.post(url=url,data= json.dumps(data),headers=headers)
    except Exception as e:
        util.log_err(str(e))
    

def signin():
    if check_env():
        usr = (get_env_values())['username']
        pwd = (get_env_values())['password']
    else :
        usr = get_username()
        pwd = get_password() 
    json_data = {"username" : usr, "password" : pwd}
    url = util.get_url('login')
    try :
        respons = requests.post(url,json_data)
        respons = respons.json()
    except Exception as e:
        msg = "Login failure ! \n"+str(e)
        print(msg)
        return util.generate_respons(False,msg)
    else :
        if respons["code"] != 200 :
            print(respons["message"])
            return util.generate_respons(False,respons["message"])
        data = respons["data"]
        send_todb(data['user_id'], data['project_id'])
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S%f")
        create_env_file(usr,pwd, data["user_id"], data["project_id"], data["token"],timestamp)
        generate_session(data["user_id"], data["project_id"], data["token"] )

        return util.generate_respons(True,"success",data)
    

def generate_session(user_id, project_id, token):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S%f")
    sess =  {"user_id" : user_id, "project_id": project_id, "token" : token, "timestamp" : timestamp}
    dump_session(sess)
    return sess   

def create_env_file(username, password, user_id, project_id, token, timestamp):
    if not os.path.isdir("{}/restknot".format(DUMP_FOLDER)):
        os.mkdir("{}/restknot".format(DUMP_FOLDER))    
    try :
        env_file = open("{}/restknot/.restknot.env".format(DUMP_FOLDER),"w+")
        env_file.write("OS_USERNAME=%s\n" %username)
        env_file.write("OS_PASSWORD=%s\n" %password)
        env_file.write("OS_USER_ID=%s\n" %user_id)        
        env_file.write("OS_PROJECT_ID=%s\n" %project_id)
        env_file.write("OS_TOKEN=%s\n" %token)
        env_file.write("OS_TIMESTAMP=%s\n" %timestamp)
        env_file.close()
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
        restknot_env['user_id']  = os.environ.get('OS_USER_ID')
        restknot_env['project_id'] = os.environ.get('OS_PROJECT_ID')
        restknot_env['token']   = os.environ.get('OS_TOKEN')
        restknot_env['timestamp'] = os.environ.get('OS_TIMESTAMP')
        return restknot_env
    else:
        util.log_err("Can't find restknot.env")


def load_env_file():
    return load_dotenv("{}/restknot/.restknot.env".format(DUMP_FOLDER), override=True)

def check_env():
    return os.path.isfile("{}/restknot/.restknot.env".format(DUMP_FOLDER))

def ex_logout(r=False):
    
    if check_session():
        print('Logging Out')
        os.remove('/tmp/session.pkl')
        if r:
            os.remove("{}/restknot/.restknot.env".format(DUMP_FOLDER))
        time.sleep(1)
        sp.call('clear',shell=True)
    elif check_env() and not check_session() :
        if r:
            os.remove("{}/restknot/.restknot.env".format(DUMP_FOLDER))
        time.sleep(1)
    else:
        print("No active user")


def dump_session(sess):
    try:
        with open('/tmp/session.pkl','wb') as f:
            dill.dump(sess, f, protocol=2)
    except Exception as e:
        util.log_err("Dump session failed")

def check_session():
    return os.path.isfile("/tmp/session.pkl")

def load_dumped_session():
    if check_session():
        sess = None
        with open('/tmp/session.pkl', 'rb') as f:
            sess = dill.load(f)
        return util.generate_respons(True,"success",sess)
    elif check_env():
        regenerate_session()  
        return load_dumped_session()
    else :
        util.log_err("Loading Session Failed")
        msg = "Please login first"
        return util.generate_respons(False,msg)

def get_token():
    result = load_dumped_session()
    try:
        token = result['data']['token']
    except Exception:
        return util.generate_respons(False,"Token Failure")
    else:
        return util.generate_respons(True,"Success",token) 

def get_headers():
    timestamp = timestamp_check()
    if not timestamp['status']:
        signin()
    try :
        token = get_token()
        user_id = get_user_id()
        headers = {"Access-Token" : token['data'], "user-id": user_id['data']}
    except Exception as e:
        return util.generate_respons(False,str(e))
    else:
        return util.generate_respons(True,'success',headers)

def get_user_id():
    result = load_dumped_session()
    try:
        user_id = result['data']['user_id']
    except Exception:
        return util.generate_respons(False,"User ID Failure")
    else:
        return util.generate_respons(True,"Success",user_id) 


def check_password(): #pragma: no cover
    print("Please re-enter password for authentication")
    pwd = (get_env_values())['password']
    pwd2 = get_password()
    if pwd == pwd2:
        return True
    else:
        print("Wrong password ")
        return False

def regenerate_session():
    try :
        env_data = get_env_values()
        generate_session(user_id=env_data['user_id'],project_id=env_data['project_id'],token=env_data['token'])
        return util.generate_respons(True,"success")
    except Exception as e:
        return util.generate_respons(False,str(e))


def timestamp_check():
    sess = get_env_values()
    sess = sess['timestamp']
    ts1 = datetime.datetime.strptime(sess,"%Y%m%d%H%M%S%f")
    ts2 = datetime.datetime.now()
    delta = (ts2-ts1)

    if delta.seconds > 3600 or delta.days > 0:
        return util.generate_respons(False,"Token expired")
    else :
        return util.generate_respons(True,"success")