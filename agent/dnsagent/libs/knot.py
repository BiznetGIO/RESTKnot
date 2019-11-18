import json

from dnsagent.libs import parser
from dnsagent.libs import command_generator as cmd_generator
from dnsagent.libs import utils


def send_command(data):
    """Send command to knot socket"""
    initialiazed_command = parser.initialiaze(data)

    try:
        knot_data = parser.execute_command(initialiazed_command)
        response = {
            "result": True,
            "description": initialiazed_command,
            "status": "Command Executed",
            "data": knot_data,
        }
        return response
    except Exception as e:
        response = {"result": False, "error": str(e), "status": "Command Failed"}
        return response


def parse_data_general(data):
    zone = None  # example.com
    zone_id = None
    command_type = None
    command = None

    for i in data:
        zone = i
        command_type = data[i]["command"]
        zone_id = data[i]["id_zone"]
        command = data[i]["general"]

    data = {"command": command, "zone": zone}
    command_data = initialiaze_command_general(data, zone_id, command_type)

    if not command_data:
        utils.log_err("Command Not Supported")
    else:
        dict_command = json.loads(command_data["data"])
        try:
            status = dict_command["status"]
        except Exception:
            status = True
        if not status:
            utils.log_err("Command Failed")
            utils.log_err(dict_command["error"])
        else:
            utils.log_info("Command Executed")


def initialiaze_command_general(data, zone_id, command_type):
    response = None
    zone = data["zone"]

    if command_type == "config":
        begin_conf_cmd, commit_conf_cmd, _ = cmd_generator.conf_command(zone)

        send_command(begin_conf_cmd)  # begin
        response = send_command(data)  # main data
        send_command(commit_conf_cmd)
    elif command_type == "zone":
        begin_zone_cmd, commit_zone_cmd = cmd_generator.zone_command(zone)
        send_command(begin_zone_cmd)  # begin
        response = send_command(data)  # main data
        send_command(commit_zone_cmd)

    return response


def parse_data_cluster(data, flags=None):
    zone = None
    id_zone = None
    json_data = None
    for i in data:
        zone = i
        id_zone = data[i]["id_zone"]
        json_data = data[i]["cluster"][flags]
    initialiaze_command_cluster(json_data, zone, id_zone, flags)


def initialiaze_command_cluster(data, zone, zone_id, flags):
    response = []

    begin_conf_cmd, commit_conf_cmd, set_conf_cmd = cmd_generator.conf_command(zone)
    send_command(begin_conf_cmd)

    insert_response = send_command(set_conf_cmd)
    response.append(insert_response)

    fileset_command = cmd_generator.file_set_command(zone, zone_id)
    file_response = send_command(fileset_command)
    response.append(file_response)

    for i in data["master"]:
        master_command = cmd_generator.set_master_command(zone, i)
        master_response = send_command(master_command)
        response.append(master_response)

    if flags == "master":
        for i in data["notify"]:
            notify_command = cmd_generator.notify_command(zone, i)
            send_command(notify_command)
            response.append(notify_command)

    for i in data["acl"]:
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
