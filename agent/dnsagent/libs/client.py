from dnsagent.libs import utils


def sendblock(ctl, commands, treturn):

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
