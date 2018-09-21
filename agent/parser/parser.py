from agent.utility import utils
from agent.control.libknot import control
from agent.control import client
import json


control.load_lib("libknot.so.7")
ctl = control.KnotCtl()
ctl.connect("/var/run/knot/knot.sock")


def check_command(command):
    sdl_data = utils.repodata()
    try:
        sdl_data[command]
    except Exception as e:
        print("illegal command : ", e)
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
    for project in obj_data:
        action_obj = list()
        for action in obj_data[project]:
            if not check_command(action):
                return None
            else:
                data_obj = dict()
                for params in obj_data[project][action]:
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
    try:
        parser_data = parser(data)
    except Exception:
        print("Error: Parameter data Needed")
    else:
        return parser_data


def get_params_block(data_params):
    parameters=dict()
    for data_parsing in data_params:
        for command in data_parsing:
            if command=='sendblock':
                for value in data_parsing[command]:
                    parameters[value]=data_parsing[command][value]
    return parameters


def get_params_recieve(data_params):
    parameters=dict()
    for data_parsing in data_params:
        for command in data_parsing:
            if command=='receive':
                for value in data_parsing[command]:
                    parameters[value]=data_parsing[command][value]
    return parameters


def execute_command(initialiaze):
    try:
        resp = None
        for data in initialiaze:
            for project in data:
                parameter_block = get_params_block(data[project])
                parameter_stats = get_params_recieve(data[project])
                if parameter_stats['type'] == 'block':
                    client.sendblock(ctl, parameter_block)
                    resp = ctl.receive_block()
                elif parameter_stats['type'] == 'stats':
                    client.sendblock(**parameter_block)
                    resp = ctl.receive_stats()
    except Exception as e:
        print(e)
    else:
        return json.dumps(resp, indent=4)
    ctl.send(control.KnotCtlType.END)
    ctl.close()
