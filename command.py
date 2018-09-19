import json
from libknot.control import *


load_lib("libknot.so.7")
ctl = KnotCtl()
ctl.connect("/var/run/knot/knot.sock")


def block_command(command, flags=None):
    try:
        ctl.send_block(cmd=command, flags=flags)
        resp = ctl.receive_block()
    except Exception as e:
        print(e)
    else:
        return json.dumps(resp, indent=4)
    finally:
        ctl.send(KnotCtlType.END)
        ctl.close()

def stats_command(command, flags=None):
    try:
        ctl.send_block(cmd=command, flags=flags)
        zone_stats = ctl.receive_stats()
    except Exception as e:
        print(e)
    else:
        return json.dumps(zone_stats, indent=4)
    finally:
        ctl.send(KnotCtlType.END)
        ctl.close()

conf_list = block_command('conf-list')
# stats_list = stats_command('stats')
print(conf_list)
# print(stats_list)