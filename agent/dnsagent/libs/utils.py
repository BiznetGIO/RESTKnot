import yaml
import os
import shutil
import coloredlogs
import logging


def check_root():
    if os.geteuid() != 0:
        log_err("You need root permissions to do this")
        exit()


def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)


def yaml_parser_file(file):
    with open(file, "r") as stream:
        try:
            data = yaml.load(stream, Loader=yaml.FullLoader)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def yaml_parser(stream):
    try:
        data = yaml.load(stream)
        print(data)
        return data
    except yaml.YAMLError as exc:
        print(exc)


def copyfile(src, dest):
    try:
        shutil.copyfile(src, dest)
    except OSError as e:
        print("Directory not copied. Error: %s" % e)


def make_archive(name, path):
    shutil.make_archive(name, "zip", path)
