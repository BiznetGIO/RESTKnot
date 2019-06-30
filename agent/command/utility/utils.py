import yaml, os
import subprocess


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

def repodata():
    abs_path = os.path.dirname(os.path.realpath(__file__))
    repo_file = "{}/templates/rules.yml".format(abs_path)
    return yaml_parser(repo_file)

def exec_shell(command):
    cmd = os.popen(command).read()
    return cmd

def exec_command_cluster(command):
    cmd = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return str(cmd.decode("utf-8"))