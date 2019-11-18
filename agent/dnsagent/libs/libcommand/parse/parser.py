import os
import json

from dnsagent.libs.libcommand.utility import utils
from dnsagent.libs.libcommand.control import client
from dnsagent.libs import utils as dnsagent_utils
from dnsagent.libs.libcommand.control.libknot.control import (
    KnotCtlError,
    KnotCtl,
    load_lib,
    KnotCtlType,
)

knot_lib = os.environ.get("RESTKNOT_KNOT_LIB", "libknot.so")
knot_socket = os.environ.get("RESTKNOT_KNOT_SOCKET", "/var/run/knot/knot.sock")
root_dir = os.path.dirname(os.path.abspath(__file__))


def is_command(command):
    """check if COMMAND available in defined rules"""
    rules = utils.get_rules()
    try:
        rules[command]
        return True
    except Exception:
        msg = f'command: "{command}" is not recognized'
        raise ValueError(msg)


def is_parameters(command, parameters):
    """check if PARAMETERS available in defined rules"""
    rules = utils.get_rules()
    try:
        rules[command]["parameters"][parameters]
        return True
    except Exception:
        msg = f'parameter: "{parameters}" is not recognized'
        raise ValueError(msg)


def initialiaze(data):
    try:
        parser_data = parse_json(data)
    except Exception as e:
        raise e
    else:
        return parser_data


def get_params_block(data_params):
    parameters = dict()
    for data_parsing in data_params:
        for command in data_parsing:
            if command == "sendblock":
                for value in data_parsing[command]:
                    parameters[value] = data_parsing[command][value]
    return parameters


def get_params_recieve(data_params):
    parameters = dict()
    for data_parsing in data_params:
        for command in data_parsing:
            if command == "receive":
                for value in data_parsing[command]:
                    parameters[value] = data_parsing[command][value]
    return parameters


def parse_json(data):
    commands = []

    # command: command-commit | zone-begin
    for command in data:
        actions = []
        # action: sendblock | receive
        for action in data[command]:
            if not is_command(action):
                return None

            data_obj = dict()
            # params: cmd | item | section | data | type
            for params in data[command][action]:
                if not is_parameters(action, params):
                    return None
                data_obj[params] = data[command][action][params]

            actions.append({action: data_obj})

        command_type = data[command]["receive"]["type"]  # .e.g block
        if command_type == "command":
            # FIXME is this subprocess thing still used?
            cli_shell = parse_command_zone(actions[0]["sendblock"])
            exec_cliss = utils.exec_shell(cli_shell)
            commands.append({"type": "general", command: str(exec_cliss)})
            return commands
        else:
            commands.append({command: actions})
            return commands


def parse_command_zone(json_data):
    cmd = json_data["cmd"]
    zone = json_data["zone"]
    own = json_data["owner"]
    data = json_data["data"]
    rtype = json_data["rtype"]
    ttl = json_data["ttl"]
    owner = ""
    if own == zone:
        owner = zone
        cli_shell = (
            "knotc "
            + cmd
            + " "
            + zone
            + ". "
            + owner
            + ". "
            + ttl
            + " "
            + rtype
            + " "
            + data
        )
    elif own == "@":
        owner = own
        cli_shell = (
            "knotc "
            + cmd
            + " "
            + zone
            + ". "
            + owner
            + " "
            + ttl
            + " "
            + rtype
            + " "
            + data
        )
    elif rtype == "cluster":
        cli_shell = own + "_" + data + ".sh " + zone
    elif cmd == "unset-cluster":
        cli_shell = "unset_cluster.sh " + zone
    else:
        if rtype == "notify" and own == "slave":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].master' " + data
        elif rtype == "notify" and own == "master":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].notify' " + data
        elif rtype == "acl" and own == "master":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].acl' " + data
        elif rtype == "acl" and own == "slave":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].acl' " + data
        elif rtype == "file" and own == "all":
            cli_shell = (
                "knotc " + cmd + " 'zone[" + zone + "].file' '" + zone + ".zone'"
            )
        elif rtype == "module" and own == "all":
            cli_shell = (
                "knotc " + cmd + " 'zone[" + zone + "].module' 'mod-stats/default'"
            )
        else:
            owner = json_data["owner"] + "." + zone
            cli_shell = (
                "knotc "
                + cmd
                + " "
                + zone
                + ". "
                + owner
                + ". "
                + ttl
                + " "
                + rtype
                + " "
                + data
            )
    return cli_shell


def execute_command(initialiaze):
    load_lib(knot_lib)
    ctl = KnotCtl()
    try:
        ctl.connect(knot_socket)
    except KnotCtlError as e:
        dnsagent_utils.log_err(str(e))
    try:
        resp = None
        no = 0
        for data in initialiaze:
            no = no + 1
            parameter_block = None
            parameter_stats = None
            for project in data:
                parameter_block = get_params_block(data[project])
                parameter_stats = get_params_recieve(data[project])
                resp = client.sendblock(ctl, parameter_block, parameter_stats["type"])
    except KnotCtlError as e:
        resp = {"status": False, "error": str(e)}
        return json.dumps(resp, indent=4)
    else:
        ctl.send(KnotCtlType.END)
        ctl.close()
        return json.dumps(resp, indent=4)
