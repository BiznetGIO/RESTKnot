import json, os
from domba.libs import utils

def sendblock(ctl,params, treturn):
    data1=None
    try:
        data1 = params['data']
    except Exception:
        data1 = None

    try:
        cmd= params['cmd']
    except Exception as e:
        print("CMD Parameters needed "+e)

    try:
        pass
    except Exception:
        pass

    try:
        section = params['section']
    except Exception:
        section=None

    try:
        item = params['item']
    except Exception:
        item=None

    try:
        identifier = params['identifier']
    except Exception:
        identifier=None

    try:
        zone = params['zone']
    except Exception:
        zone=None

    try:
        owner = params['owner']
    except Exception:
        owner=None

    try:
        ttl = params['ttl']
    except Exception:
        ttl=None

    try:
        rtype = params['rtype']
    except Exception:
        rtype=None

    try:
        flags = params['flags']
    except Exception:
        flags=None

    try:
        filters = params['filter']
    except Exception:
        filters=None

    resp = None

    try:
        ctl.send_block(cmd=cmd, section=section, item=item, identifier=identifier, zone=zone,
                        owner=owner, ttl=ttl, rtype=rtype, data=data1, flags=flags,
                        filter=filters)
    except Exception as e:
        utils.log_err(e)
    if treturn == 'block':
        resp = ctl.receive_block()
    elif treturn == 'stats':
        resp = ctl.receive_stats()
    return resp


