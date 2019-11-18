import json

from dnsagent.libs.libcommand.parse import parser
from dnsagent.libs import command_lib
from dnsagent.libs import utils
from dnsagent.libs import command_generator as cmd_generator


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
        begin_conf_command, commit_conf_command = cmd_generator.generate_conf_command(
            zone
        )

        send_command(begin_conf_command)  # begin
        response = send_command(data)  # main data
        send_command(commit_conf_command)
    elif command_type == "zone":
        begin_zone_command, commit_zone_command = cmd_generator.generate_zone_command(
            zone
        )
        send_command(begin_zone_command)  # begin
        response = send_command(data)  # main data
        send_command(commit_zone_command)

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


def initialiaze_command_cluster(data, zone, id_zone, flags):
    if flags == "slave":
        slave_response = list()
        begin(zone)
        insert_config = command_lib.insert_config_zone(zone)
        insert_exe = libknot_json(insert_config)
        slave_response.append(insert_exe)
        file_config = command_lib.set_file(zone, id_zone)
        file_exec = libknot_json(file_config)
        slave_response.append(file_exec)
        for i in data["master"]:
            master_config = command_lib.master_create_json(zone, i)
            slave_response.append(libknot_json(master_config))
        for i in data["acl"]:
            acl_config = command_lib.create_json_acl(zone, i)
            slave_response.append(libknot_json(acl_config))
        module_config = command_lib.set_mods_stats(zone, "mod-stats/default")
        slave_response.append(libknot_json(module_config))
        serial_config = command_lib.set_serial_policy(zone, "dateserial")
        slave_response.append(libknot_json(serial_config))
        commit(zone)
        return slave_response
    else:
        master_response = list()
        begin(zone)
        insert_config = command_lib.insert_config_zone(zone)
        insert_exe = libknot_json(insert_config)
        master_response.append(insert_exe)
        file_config = command_lib.set_file(zone, id_zone)
        file_exec = libknot_json(file_config)
        master_response.append(file_exec)
        if data["master"]:
            for i in data["master"]:
                master_config = command_lib.master_create_json(zone, i)
                master_response.append(libknot_json(master_config))
        for i in data["notify"]:
            notify_config = command_lib.create_json_notify(zone, i)
            master_response.append(libknot_json(notify_config))
        for i in data["acl"]:
            acl_config = command_lib.create_json_acl(zone, i)
            master_response.append(libknot_json(acl_config))
        module_config = command_lib.set_mods_stats(zone, "mod-stats/default")
        master_response.append(libknot_json(module_config))
        serial_config = command_lib.set_serial_policy(zone, "dateserial")
        master_response.append(libknot_json(serial_config))
        commit(zone)
        return master_response
