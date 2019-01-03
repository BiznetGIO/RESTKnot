from flask_script import Command, Option
from shutil import copyfile
import os, sys


class CreateEnvironment(Command):
    option_list = (
        Option('--env', '-e', dest='env'),
        Option('--srv', '-s', dest='srv'),
    )

    def run(self, env, srv):
        pwd = os.path.dirname(os.path.realpath(__file__))
        file_path = None

        if srv == 'docker':
            file_path = pwd+"/environment/"+env+"/.env.docker"
        elif srv == 'local':
            file_path = pwd+"/environment/"+env+"/.env.example"

        dest_path = pwd+"/.env"

        try:
            copyfile(file_path, dest_path)
        except Exception as e:
            print("Seten Error: ", str(e))
        else:
            print("Setenv Success")


class GunicornServer(Command):
    """Run the app within Gunicorn"""
    def run(self, *args, **kwargs):
        pass