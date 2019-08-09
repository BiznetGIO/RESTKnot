import yaml
import os

def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            return data
        except yaml.YAMLError as exc:
            print(exc)

def repodata():
    abs_path = os.path.dirname(os.path.realpath(__file__))
    repo_file = "{}/templates/rules.yml".format(abs_path)
    return yaml_parser(repo_file)

def exec_shell(command):
    cmd = os.popen(command).read()
    return cmd

