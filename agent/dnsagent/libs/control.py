import json
import os
import time
import logging

import libknot
import libknot.control

logger = logging.getLogger(__name__)


def connect_knot():
    libknot_binary_path = os.environ.get("RESTKNOT_KNOT_LIB", "libknot.so")
    knot_socket_path = os.environ.get("RESTKNOT_KNOT_SOCKET", "/var/run/knot/knot.sock")
    knot_socket_timeout = int(os.environ.get("RESTKNOT_SOCKET_TIMEOUT", 2000))
    knot_socket_retry = int(os.environ.get("RESTKNOT_SOCKET_RETRY", 10))

    libknot.Knot(libknot_binary_path)
    knot_ctl = libknot.control.KnotCtl()

    attempts = 0
    err_msg = "Can't connect to knot socket"
    while attempts < knot_socket_retry:
        time.sleep(5)

        try:
            knot_ctl.connect(knot_socket_path)
            knot_ctl.set_timeout(knot_socket_timeout)
            return knot_ctl
        except libknot.control.KnotCtlError as e:
            attempts += 1
            logger.info(f"{err_msg}: {e}. Attempts: {attempts}")

    raise ValueError(f"{err_msg}")


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
            flags="B",
            filter=filter_,
        )
        resp_ = ctl.receive_block()
        if resp_:
            resp = json.dumps(resp, indent=4)
    except libknot.control.KnotCtlError as knot_error:
        # most of the time, after removing a zone
        # socket connection will be time out
        resp = str(knot_error.data)
    finally:
        ctl.send(libknot.control.KnotCtlType.END)
        ctl.close()
        return resp
