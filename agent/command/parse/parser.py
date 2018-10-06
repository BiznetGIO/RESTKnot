from command.utility import utils
from command.control.libknot import control
from command.control import client
import json, os


def tes_conn():
    control.load_lib("libknot.so.7")
    ctl = control.KnotCtl()
    # ctl.connect(str(os.getenv('KNOT_SOCKET')))
    ctl.connect("/var/run/knot/knot.sock")
    try:
        # ctl.send_block(cmd="conf-begin")
        # resp = ctl.receive_block()

        # ctl.send_block(cmd="conf-set", section="zone", item="domain", data="ianktesting.com")
        # resp = ctl.receive_block()

        # ctl.send_block(cmd="conf-commit")
        # resp = ctl.receive_block()

        # ctl.send_block(cmd="conf-read", section="zone", item="domain")
        # resp = ctl.receive_block()

        ctl.send_block(cmd="zone-begin", data="ianktesting.com")
        resp = ctl.receive_block()

        ctl.send_block(cmd="zone-set", data="ianktesting.com. ianktesting.com. 800 A 10.10.10.10")
        resp = ctl.receive_block()

        ctl.send_block(cmd="zone-commit", data="ianktesting.com")
        resp = ctl.receive_block()

        print(json.dumps(resp, indent=4))
    except Exception as e:
        print(e)
    finally:
        ctl.send(control.KnotCtlType.END)
        ctl.close()

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

def initialiaze(data):
    try:
        parser_data = parser_json(data)
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

def parser_json(obj_data):
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

def execute_command(initialiaze):
    control.load_lib("libknot.so.7")
    ctl = control.KnotCtl()
    # ctl.connect(str(os.getenv('KNOT_SOCKET')))
    ctl.connect("/var/run/knot/knot.sock")
    try:
        resp = None
        for data in initialiaze:
            parameter_block = None
            parameter_stats = None
            for project in data:
                parameter_block = get_params_block(data[project])
                parameter_stats = get_params_recieve(data[project])
                resp = client.sendblock(ctl, parameter_block, parameter_stats['type'])
    except Exception as e:
        print("Error: ",e)

    ctl.send(control.KnotCtlType.END)
    ctl.close()
    return json.dumps(resp, indent=4)
