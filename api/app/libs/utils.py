import yaml, os,hashlib
from app import root_dir
from datetime import datetime
import json, requests
import re
from ipaddress import ip_address

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

def reposlave():
    abs_path = root_dir
    repo_file = "{}/static/cluster/slave.yml".format(abs_path)
    return yaml_parser(repo_file)

def repomaster():
    abs_path = root_dir
    repo_file = "{}/static/cluster/master.yml".format(abs_path)
    return yaml_parser(repo_file)

def get_command(req):
    command = req.split("/")
    command = command[2]
    return command

def get_tag():
    return hashlib.md5(str(timeset()).encode('utf-8')).hexdigest()


def send_http_cmd(url, data, headers=None):
    json_data = json.dumps(data)
    try:
        send = requests.post(url, data=json_data, headers=headers)
        respons = send.json()
        type_command = respons['data'][0]['type']
        if type_command == "general":
            return respons
        else:
            data = None
    except requests.exceptions.RequestException as e:
        respons = {
            "result": False,
            "Error": str(e),
            "description": None
        }
        return respons
    

def send_http_clusters(url, data, headers=None):
    respons = None
    send = None
    json_data = json.dumps(data)
    data = None
    try:
        send = requests.post(url, data=json_data, headers=headers)
        response_time = send.elapsed.total_seconds()
        respons = send.json()
        try:
            data = respons['data']
        except Exception as e:
            data = None
        else:
            for i in data:
                check_command_error = None
                try:
                    if i['data']['status'] == False:
                        check_command_error = True
                except Exception as e:
                    check_command_error = False

                if check_command_error:
                    respons['data'] = {
                        "status": False,
                        "description": i['description'],
                        "error": i['data']['error'],
                        "result": "Command Not Execute",
                        "time": response_time
                    }
                    return respons['data']
                else:
                    resulsts ={
                        "data": respons,
                        "times": response_time
                    }
                    return resulsts
    except requests.exceptions.RequestException as e:
        respons = {
            "result": False,
            "Error": str(e),
            "description": None
        }
        return respons

def send_http(url, data, headers=None):
    respons = None
    send = None
    json_data = json.dumps(data)
    data = None
    try:
        send = requests.post(url, data=json_data, headers=headers)
        response_time = send.elapsed.total_seconds()
        respons = send.json()
        try:
            data = respons['data']
        except Exception as e:
            data = None
        else:
            respons['data'] = data
            check_command_error = None
            try:
                if respons['data']['status'] == False:
                    check_command_error = True
            except Exception as e:
                check_command_error = False

            if check_command_error:
                respons['data'] = {
                    "status": False,
                    "description": respons['description'],
                    "error": respons['data']['error'],
                    "result": "Command Not Execute",
                    "time": response_time
                }
                return respons['data']
            else:
                return respons
    except requests.exceptions.RequestException as e:
        respons = {
            "result": False,
            "Error": str(e),
            "description": None
        }
        return respons

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

def domain_validation(domain):
    pattern = re.compile("^(?!(https:\/\/|http:\/\/|www\.|mailto:|smtp:|ftp:\/\/|ftps:\/\/))(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))$")
    if pattern.match(domain):
        return True
    else:
        return False

def cname_validation(cname):
    if cname == '@':
        return True
    else:
        pattern = re.compile("^(([a-zA-Z0-9_]|[a-zA-Z_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z_\*][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$")
        if pattern.match(cname):
            return True
        else:
            return False

def record_validation(record) :
    if record == '@' or record=='*':
        return True
    else:
        pattern = re.compile("^(([\*a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[_A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
        if pattern.match(record):
            return True
        else:
            return False

def mx_validation(mx):
    if mx == '@':
        return True
    else:
        pattern = re.compile("^(([a-zA-Z0-9_]|[a-zA-Z0-9_][a-zA-Z0-9_\-]*[a-zA-Z0-9_])\.)*([A-Za-z0-9_]|[A-Za-z0-9_\*][A-Za-z0-9_\-]*[A-Za-z0-9_](\.?))$")
        if pattern.match(mx):
            return True
        else:
            return False

def txt_validation(txt):
    if txt == '@' or txt=='*':
        return True
    else:
        pattern = re.compile("^[\x20-\x7F]*$")
        if pattern.match(txt):
            return True
        else:
            return False