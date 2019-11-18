import os
import json

from dnsagent.libs import utils
from dnsagent.libs import client
from dnsagent.vendor.libknot import control as knotlib


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
            print("I AM CLI THINGS!")
            # FIXME is this subprocess thing still used?
            # I don't find any command_type == 'command' in the API sender
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
    owner_type = json_data["owner"]
    data = json_data["data"]
    rtype = json_data["rtype"]
    ttl = json_data["ttl"]
    owner = ""

    if owner_type == zone:
        owner = zone
        cli_shell = f"knotc {cmd} {zone}. {owner}. {ttl} {rtype} {data}"
    elif owner_type == "@":
        owner = owner_type
        cli_shell = f"knotc {cmd} {zone}. {owner} {ttl} {rtype} {data}"
    elif rtype == "cluster":
        cli_shell = owner_type + "_" + data + ".sh " + zone
    elif cmd == "unset-cluster":
        cli_shell = "unset_cluster.sh " + zone
    else:
        if rtype == "notify" and owner_type == "slave":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].master' " + data
        elif rtype == "notify" and owner_type == "master":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].notify' " + data
        elif rtype == "acl" and owner_type == "master":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].acl' " + data
        elif rtype == "acl" and owner_type == "slave":
            cli_shell = "knotc " + cmd + " 'zone[" + zone + "].acl' " + data
        elif rtype == "file" and owner_type == "all":
            cli_shell = (
                "knotc " + cmd + " 'zone[" + zone + "].file' '" + zone + ".zone'"
            )
        elif rtype == "module" and owner_type == "all":
            cli_shell = (
                "knotc " + cmd + " 'zone[" + zone + "].module' 'mod-stats/default'"
            )
        else:
            owner = json_data["owner"] + "." + zone
            cli_shell = f"knotc {cmd} {zone}. {owner}. {ttl} {rtype} {data}"
    return cli_shell


def execute_command(command):
    libknot_binary_path = os.environ.get("RESTKNOT_KNOT_LIB", "libknot.so")
    knot_socket_path = os.environ.get("RESTKNOT_KNOT_SOCKET", "/var/run/knot/knot.sock")

    knotlib.load_lib(libknot_binary_path)
    ctl = knotlib.KnotCtl()
    try:
        ctl.connect(knot_socket_path)
    except knotlib.KnotCtlError as e:
        raise ValueError(f"Can't connect to knot socket: {e}")

    try:
        resp = None
        for data in command:
            parameter_block = None
            parameter_stats = None

            for project in data:
                parameter_block = get_params_block(data[project])
                parameter_stats = get_params_recieve(data[project])
                resp = client.sendblock(ctl, parameter_block, parameter_stats["type"])
    except knotlib.KnotCtlError as e:
        resp = {"status": False, "error": str(e)}
        return json.dumps(resp, indent=4)
    else:
        ctl.send(knotlib.KnotCtlType.END)
        ctl.close()
        return json.dumps(resp, indent=4)
