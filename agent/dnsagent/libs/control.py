import os
import json

from dnsagent.vendor.libknot import control as knotlib


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


def send_block(
    cmd=None,
    section=None,
    item=None,
    identifier=None,
    zone=None,
    owner=None,
    ttl=None,
    rtype=None,
    data=None,
    flags=None,
    filter_=None,
):
    """Send block command to Libknot server control."""

    ctl = connect_knot()
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
            filter=filter_,
        )
        resp = ctl.receive_block()
    except knotlib.KnotCtlError as e:
        raise ValueError(f"{e}")
    else:
        ctl.send(knotlib.KnotCtlType.END)
        ctl.close()
        return json.dumps(resp, indent=4)
