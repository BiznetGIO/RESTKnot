import yaml
import os
import shutil
import zipfile
import coloredlogs
import logging
import codecs
from dotenv import load_dotenv
import subprocess

APP_HOME = os.path.expanduser("~")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def check_root():
    if os.geteuid() != 0:
        log_err("You need root permissions to do this")
        exit()

def exec_command_cluster(command):
    cmd = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return str(cmd.decode("utf-8"))

def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)


def get_index(dictionary):
    return [key for (key, value) in dictionary.items()]


def isint(number):
    try:
        to_float = float(number)
        to_int = int(to_float)
    except ValueError:
        return False
    else:
        return to_float == to_int

def isfloat(number):
    try:
        float(number)
    except ValueError:
        return False
    else:
        return True


def check_key(dict, val):
    try:
        if dict[val]:
            return True
    except Exception:
        return False

def question(word): 
    answer = False
    while answer not in ["y", "n"]:
        answer = input("{} [y/n]? ".format(word)).lower().strip()

    if answer == "y":
        answer = True
    else:
        answer = False
    return answer

def log_info(stdin):
    coloredlogs.install()
    logging.info(stdin)


def log_warn(stdin):
    coloredlogs.install()
    logging.warn(stdin)


def log_err(stdin):
    coloredlogs.install()
    logging.error(stdin)

def check_keys(obj, keys):
    try:
        obj[keys]
    except Exception:
        return False
    else:
        return True

def yaml_parser_file(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream, Loader= yaml.FullLoader)
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


def yaml_create(stream, path):
    with open(path, 'w') as outfile:
        try:
            yaml.dump(stream, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return True


def yaml_writeln(stream, path):
    with open(path, '+a') as outfile:
        try:
            yaml.dump(stream, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return True


def yaml_read(path):
    with open(path, 'r') as outfile:
        try:
            data = yaml.load(outfile)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return data

def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def copyfile(src, dest):
    try:
        shutil.copyfile(src, dest)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def read_file(file):
    if os.path.isfile(file):
        return True
    else:
        return False


def create_file(file, path, value=None):
    f=open(path+"/"+file, "a+")
    f.write(value)
    f.close()
    try:
        return read_file(path+"/"+file)
    except Exception as e:
        print(e)


def check_folder(path):
    return os.path.isdir(path)


def create_folder(path):
    return os.makedirs(path)


def remove_folder(path):
    return shutil.rmtree(path)


def read_value(file):
    value = open(file)
    return value.read()


def check_env(stack):
    return os.path.isfile("{}/.domba/{}.env".format(APP_HOME, stack))


def load_env_file(stack):
    return load_dotenv("{}/.domba/{}.env".format(APP_HOME, stack), override=True)

def get_env_values_knot():
    if check_env("knot"):
        load_env_file("knot")
        domba_env = {}
        domba_env['knot_lib'] = os.environ.get('OS_KNOT_LIB')
        domba_env['knot_sock'] = os.environ.get('OS_KNOT_SOCKS')
        return domba_env
    else:
        print("Can't find knot.env")

def get_env_values_broker():
    if check_env("broker"):
        load_env_file("broker")
        domba_env = {}
        domba_env['broker'] = os.environ.get('OS_BROKER')
        domba_env['port'] = os.environ.get('OS_PORTS')
        domba_env['topic'] = os.environ.get('OS_TOPIC')
        domba_env['group'] = os.environ.get('OS_GROUP')
        domba_env['flags'] = os.environ.get('OS_FLAGS')
        return domba_env
    else:
        print("Can't find broker.env")


def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            data = {
                "index": file,
                "dirs": dirs,
                "file": os.path.join(root, file)
            }
            listdir.append(data)
    return listdir


def make_archive(name, path):
    shutil.make_archive(name,"zip",path)


