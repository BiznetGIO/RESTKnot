from dnsagent.libs import utils


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


def initialiaze(command):
    try:
        parsed_command = parse_json(command)
    except Exception as e:
        raise e
    else:
        return parsed_command


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


def parse_json(command):
    parsed_command = []

    # command: command-commit | zone-begin
    for command_ in command:
        actions = []
        # action: sendblock | receive
        for action in command[command_]:
            if not is_command(action):
                return None

            data_obj = dict()
            # params: cmd | item | section | data | type
            for params in command[command_][action]:
                if not is_parameters(action, params):
                    return None
                data_obj[params] = command[command_][action][params]

            actions.append({action: data_obj})

        command_type = command[command_]["receive"]["type"]  # .e.g block
        if command_type == "command":
            print("I AM CLI THINGS!")
            # FIXME is this subprocess thing still used?
            # I don't find any command_type == 'command' in the API sender
            cli_shell = parse_command_zone(actions[0]["sendblock"])
            exec_cliss = utils.exec_shell(cli_shell)
            parsed_command.append({"type": "general", command_: str(exec_cliss)})
            return parsed_command
        else:
            parsed_command.append({command_: actions})
            return parsed_command


def parse_command_zone(json_data):
    # FIXME is this subprocess thing still used?
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
