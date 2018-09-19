import json
from libs.command.libknot.control import *


load_lib("libknot.so.7")
ctl = KnotCtl()
ctl.connect("/var/run/knot/knot.sock")


def block_command(cmd=None, flags=None,section=None,
                    item=None, identifier=None, zone=None,
                    owner=None, ttl=None, rtype=None, data=None,
                    filter=None):
    print(cmd)
    print(section)
    print(item)
    print(data)
    # try:
    #     ctl.send_block(cmd="conf-begin")
    #     resp = ctl.receive_block()
    #     # ctl.send_block(cmd="conf-set", section="zone", item="domain", data="test12")
    #     # resp = ctl.receive_block()
    #     # ctl.send_block(cmd="conf-commit")
    #     # resp = ctl.receive_block()
    #     # ctl.send_block(cmd="conf-read", section="zone", item="domain")
    #     # resp = ctl.receive_block()
    #     print(json.dumps(resp, indent=4))
    # finally:
    #     ctl.send(KnotCtlType.END)
    #     ctl.close()


def stats_command(cmd, flags=None, section=None,
                    item=None, identifier=None, zone=None,
                    owner=None, ttl=None, rtype=None, data=None,
                    filter=None):
    stats_data = dict()
    try:
        ctl.send_block(cmd=cmd, flags=flags, section=section,
                    item=item, identifier=identifier, zone=zone,
                    owner=owner, ttl=ttl, rtype=rtype, data=data,
                    filter=filter)
        stats_data = ctl.receive_stats()
    except:
        pass

    ctl.send(KnotCtlType.END)
    ctl.close()

    stats = {
        "data": stats_data
    }

    return json.dumps(stats, indent=4, sort_keys=True)
