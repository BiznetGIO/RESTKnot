from __future__ import unicode_literals
from prompt_toolkit.shortcuts import confirm

import getpass
import os
import requests
import dill
from dotenv import load_dotenv
from libs import utils as util
import subprocess as sp
import time
from cmd import Cmd

DUMP_FOLDER = os.path.expanduser("~")

def get_username():
    usr = raw_input("username : ")
    usr = str(usr)
    return usr

def get_password():
    return getpass.getpass("password : ")


def send_todb(user_id,project_id) : 
    data = {"project_id" : project_id , "user_id" : user_id}
    headers = {'Content-Type': "application/json"}
    try :
        url = util.get_url('user')
        requests.post(url=url,data= data, headers=headers)
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
        respons = str(e)
        print("Login Failure !")
        exit()
    if respons["code"] != 200 :
        print(respons["message"])
        exit()
    else :
        respons = respons["data"]
        send_todb(respons['user_id'], respons['project_id'])
        create_env_file(usr,pwd, respons["user_id"], respons["project_id"], respons["token"])
        generate_session(respons["user_id"], respons["project_id"], respons["token"] )
        return
    

def generate_session(user_id, project_id, token):
    sess =  {"user_id" : user_id, "project_id": project_id, "token" : token}
    dump_session(sess)   

def create_env_file(username, password, user_id, project_id, token):
    if not os.path.isdir("{}/restknot".format(DUMP_FOLDER)):
        os.mkdir("{}/restknot".format(DUMP_FOLDER))    
    try :
        env_file = open("{}/restknot/.restknot.env".format(DUMP_FOLDER),"w+")
        env_file.write("OS_USERNAME=%s\n" %username)
        env_file.write("OS_PASSWORD=%s\n" %password)
        env_file.write("OS_USER_ID=%s\n" %user_id)        
        env_file.write("OS_PROJECT_ID=%s\n" %project_id)
        env_file.write("OS_TOKEN=%s\n" %token)
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
    else :
        print("No active user")


def dump_session(sess):
    try:
        with open('/tmp/session.pkl','wb') as f:
            dill.dump(sess, f)
    except Exception as e:
        util.log_err("Dump session failed")

def check_session():
    return os.path.isfile("/tmp/session.pkl")

def load_dumped_session():
    try:
        if check_session():
            sess = None
            with open('/tmp/session.pkl', 'rb') as f:
                sess = dill.load(f)
            return sess
        else:
            if check_env():
                signin()    
            return load_dumped_session()
    except Exception as e:
        util.log_err("Loading Session Failed")
        util.log_err("Please login first")
        util.log_err(str(e))
        exit()

def get_token():
    token = load_dumped_session()
    return token['token']

def get_headers():
    headers = {"Access-Token" : get_token(), "user-id": get_user_id()}
    return headers

def get_user_id():
    user_id = load_dumped_session()
    return user_id['user_id']

def check_password():
    print("Please re-enter password for authentication")
    pwd = (get_env_values())['password']
    pwd2 = get_password()
    if pwd == pwd2:
        return True
    else:
        print("Wrong password ")
        return False