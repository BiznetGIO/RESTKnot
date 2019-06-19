import yaml, os,hashlib
from app import root_dir
from datetime import datetime
import json, requests
import re
from ipaddress import ip_address
from fqdn import FQDN

def timeset():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()

def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            listdir.append(os.path.join(root, file))
    return listdir

def repoknot():
    abs_path = root_dir
    repo_file = "{}/static/templates/knot.yml".format(abs_path)
    return yaml_parser(repo_file)

def repodata():
    abs_path = root_dir
    repo_file = "{}/static/templates/endpoint.yml".format(abs_path)
    return yaml_parser(repo_file)

def repodefault():
    abs_path = root_dir
    repo_file = "{}/static/templates/default.yml".format(abs_path)
    return yaml_parser(repo_file)

def get_command(req):
    command = req.split("/")
    command = command[2]
    return command

def get_tag():
    return hashlib.md5(str(timeset()).encode('utf-8')).hexdigest()

# def tag_measurement(data):
#     for i in data:
#         measurement = i['measurement']
#         tags = i['tags']
#     return measurement, tags

def send_http(url, data, headers=None):
    respons = None
    send = None
    json_data = json.dumps(data)
    data = None
    try:
        send = requests.post(url, data=json_data, headers=headers)
        respons = send.json()
        try:
            data = json.loads(respons['data'])
        except Exception as e:
            raise
        else:
            data_error = None
            respons['data'] = data
            
            try:
                data_error = respons['description'][0]['cluster-set']
            except Exception:
                data_error = None
            if data_error:
                check_error = data_error.split(":")
                if check_error[0] == 'error':
                    respons['data'] = {
                        "result": False,
                        "description": data_error,
                        "status": "Command Not Execute"
                    }
                    return respons['data']
                else:
                    return respons
            else:
                return respons
    except requests.exceptions.RequestException as e:
        respons = {
            "result": False,
            "Error": str(e),
            "description": None
        }
        data = respons
        return data

def change_state(field, field_value, state):
    data_state = {
        "where":{
            field : str(field_value)
        },
        "data":{
            "state" : str(state)
        }
    }
    return data_state

def a_record_validation(a_content):
    a_cont = None
    try:
        ip_address(a_content)
    except ValueError:
        a_cont = False
    else:
        a_cont = True
    return a_cont
    # if a_cont:
    #     return True
    # else:
    #     check_fqdn = FQDN(a_content)
    #     if check_fqdn.is_valid:
    #         return True
    #     else:
    #         return False