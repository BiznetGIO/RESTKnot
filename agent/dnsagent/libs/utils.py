import yaml
import os
import coloredlogs
import logging


def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)


def yaml_parser(file):
    with open(file, "r") as stream:
        try:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def get_rules():
    abs_path = os.path.dirname(os.path.realpath(__file__))
    repo_file = "{}/templates/rules.yml".format(abs_path)
    return yaml_parser(repo_file)
