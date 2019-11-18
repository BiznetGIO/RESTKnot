import json

from dnsagent.libs import parser
from dnsagent.libs import control
from dnsagent.libs import command_generator as cmd_generator
from dnsagent.libs import utils


def send_command(command):
    """Send command to knot socket"""
    initialiazed_command = parser.initialiaze(command)

    try:
        response_ = control.execute_command(initialiazed_command)
        response = {
            "result": True,
            "description": initialiazed_command,
            "status": "Command Executed",
            "data": response_,
        }
        return response
    except Exception as e:
        response = {"result": False, "error": str(e), "status": "Command Failed"}
        return response


def extract_message(message):
    zone = None  # example.com

    for item in message:
        zone = item
        command_type = message[item].get("command", None)
        zone_id = message[item].get("id_zone", None)
        command = message[item].get("general", None)

    cmd_and_zone = {"command": command, "zone": zone}

    return cmd_and_zone, zone_id, command_type


def execute_general(message):

    cmd_and_zone, zone_id, command_type = extract_message(message)
    response = execute_command_general(cmd_and_zone, zone_id, command_type)

    if not response:
        utils.log_err("Command Not Supported")
    else:
        dict_command = json.loads(response["data"])
        try:
            status = dict_command["status"]
        except Exception:
            status = True

        if not status:
            utils.log_err("Command Failed")
            utils.log_err(dict_command["error"])
        else:
            utils.log_info("Command Executed")


def execute_command_general(cmd_and_zone, zone_id, command_type):
    response = None
    zone = cmd_and_zone.get("zone", None)

    if command_type == "config":
        begin_conf_cmd, commit_conf_cmd, _ = cmd_generator.conf_command(zone)

        send_command(begin_conf_cmd)  # begin
        response = send_command(cmd_and_zone)  # main data
        send_command(commit_conf_cmd)

    elif command_type == "zone":
        begin_zone_cmd, commit_zone_cmd = cmd_generator.zone_command(zone)

        send_command(begin_zone_cmd)  # begin
        response = send_command(cmd_and_zone)  # main data
        send_command(commit_zone_cmd)

    return response


def execute_cluster(message, flags=None):
    zone = None

    for i in message:
        zone = i
        zone_id = message[i].get("id_zone", None)
        command = message[i]["cluster"].get(flags, None)

    execute_command_cluster(command, zone, zone_id, flags)


def execute_command_cluster(command, zone, zone_id, flags):
    response = []

    begin_conf_cmd, commit_conf_cmd, set_conf_cmd = cmd_generator.conf_command(zone)
    send_command(begin_conf_cmd)

    insert_response = send_command(set_conf_cmd)
    response.append(insert_response)

    fileset_command = cmd_generator.file_set_command(zone, zone_id)
    file_response = send_command(fileset_command)
    response.append(file_response)

    for i in command["master"]:
        master_command = cmd_generator.set_master_command(zone, i)
        master_response = send_command(master_command)
        response.append(master_response)

    if flags == "master":
        for i in command["notify"]:
            notify_command = cmd_generator.notify_command(zone, i)
            send_command(notify_command)
            response.append(notify_command)

    for i in command["acl"]:
        acl_cmd = cmd_generator.acl_command(zone, i)
        acl_response = send_command(acl_cmd)
        response.append(acl_response)

    module_cmd = cmd_generator.modstat_set(zone, "mod-stats/default")
    module_response = send_command(module_cmd)
    response.append(module_response)

    serial_cmd = cmd_generator.set_serial(zone, "dateserial")
    serial_response = send_command(serial_cmd)
    response.append(serial_response)

    send_command(commit_conf_cmd)
    return response
