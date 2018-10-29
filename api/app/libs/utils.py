import yaml, os,hashlib
from app import root_dir
from datetime import datetime

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

def get_command(req):
        command = req.split("/")
        command = command[2]
        return command

def get_tag():
        return hashlib.md5(str(timeset()).encode('utf-8')).hexdigest()
