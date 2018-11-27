import yaml, os,hashlib
from app import root_dir
from datetime import datetime
from app import sockets, BaseNamespace
import json, requests

class CmdNamespace(BaseNamespace):
    def initialize(self):
        self.response = None

    def on_response(self, *args):
        list_data = list(args)
        respons_sockets = list()
        for i in list_data:
            if i['data']['data'] == 'null':
                if i['data']['Description'] == '[]':
                    data = {
                        "command": i['data']['Description'],
                        "error": True,
                        "messages": "Block Type Command Not Parsing"
                    }
                else:
                    data = {
                        "status": True,
                        "messages": "Block Type Command Execute"
                    }
            else:
                data = {
                    "status": i['data']['result'],
                    "command": i['data']['Description'],
                    "receive": json.loads(i['data']['data'])
                }
            respons_sockets.append(data)
        self.response = respons_sockets

def sendSocket(respons):
    try:
        command = sockets.define(CmdNamespace, '/command')
        command.emit('command',respons)
        sockets.wait(seconds=1)
        socket_respons = command.response
    except Exception as e:
        print("EROR DATA",e)
    else:
        return socket_respons

def timeset():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
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

def tag_measurement(data):
    for i in data:
        measurement = i['measurement']
        tags = i['tags']
    return measurement, tags

def send_http(url, data):
    json_data = json.dumps(data)
    send = requests.post(url, data=json_data)
    respons = send.json()
    data = json.loads(respons['data'])
    respons['data'] = data
    return respons
