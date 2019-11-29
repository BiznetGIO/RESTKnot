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
            # this command type is not used anymore
            # preserved here for backward compatibility
            pass
        else:  # if command type == 'block'
            parsed_command.append({command_: actions})
            return parsed_command
