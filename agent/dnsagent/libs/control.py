import os
import json

from dnsagent.libs import utils
from dnsagent.libs import parser
from dnsagent.vendor.libknot import control as knotlib


def send_block(ctl, commands, treturn):

    data = commands.get("data", None)
    cmd = commands.get("cmd", None)
    section = commands.get("section", None)
    item = commands.get("item", None)
    identifier = commands.get("identifier", None)
    zone = commands.get("zone", None)
    owner = commands.get("owner", None)
    ttl = commands.get("ttl", None)
    rtype = commands.get("rtype", None)
    flags = commands.get("flags", None)
    filters = commands.get("filter", None)

    resp = None

    try:
        ctl.send_block(
            cmd=cmd,
            section=section,
            item=item,
            identifier=identifier,
            zone=zone,
            owner=owner,
            ttl=ttl,
            rtype=rtype,
            data=data,
            flags=flags,
            filter=filters,
        )
    except Exception as e:
        utils.log_err(e)
    if treturn == "block":
        resp = ctl.receive_block()
    elif treturn == "stats":
        resp = ctl.receive_stats()
    return resp


def connect_knot():
    libknot_binary_path = os.environ.get("RESTKNOT_KNOT_LIB", "libknot.so")
    knot_socket_path = os.environ.get("RESTKNOT_KNOT_SOCKET", "/var/run/knot/knot.sock")

    knotlib.load_lib(libknot_binary_path)
    knot_ctl = knotlib.KnotCtl()

    try:
        knot_ctl.connect(knot_socket_path)
        return knot_ctl
    except knotlib.KnotCtlError as e:
        raise ValueError(f"Can't connect to knot socket: {e}")


def execute_command(command):
    knot_ctl = connect_knot()

    try:
        resp = None
        for data in command:
            parameter_block = None
            parameter_stats = None

            for project in data:
                parameter_block = parser.get_params_block(data[project])
                parameter_stats = parser.get_params_recieve(data[project])
                resp = send_block(knot_ctl, parameter_block, parameter_stats["type"])
    except knotlib.KnotCtlError as e:
        resp = {"status": False, "error": str(e)}
        return json.dumps(resp, indent=4)
    else:
        knot_ctl.send(knotlib.KnotCtlType.END)
        knot_ctl.close()
        return json.dumps(resp, indent=4)
