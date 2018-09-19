from libs.utility import utils
from libs.command import action
import json


def check_command(command):
    sdl_data = utils.repodata()
    try:
        sdl_data[command]
    except Exception as e:
        print("illigal command : ", e)
    else:
        return True

def check_parameters(command,parameters):
    sdl_data = utils.repodata()
    try:
        sdl_data[command]['parameters'][parameters]
    except Exception as e:
        print("illegal parameter : ",e)
    else:
        return True

def parser(obj_data):
    projec_obj = list()
    for project in obj_data: # ambil index project
        action_obj = list()
        for action in obj_data[project]: # ambil index aksi
            if not check_command(action):
                return None
            else:
                data_obj = dict()
                for params in obj_data[project][action]: # ambil index parameter
                    if not check_parameters(action,params):
                        return None
                    else:
                        data_obj[params]=obj_data[project][action][params]
                action_obj.append({
                    action: data_obj
                })
        projec_obj.append({
            project: action_obj
        })
    return projec_obj


def initialiaze(data):
    print(data)
    try:
        parser_data = parser(data)
    except Exception:
        print("Error: Parameter data Needed")
    else:
        return parser_data


