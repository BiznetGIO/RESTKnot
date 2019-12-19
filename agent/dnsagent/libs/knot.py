from dnsagent.libs import control


def execute(message):
    control.send_block(
        cmd=message.get("cmd"),
        section=message.get("section"),
        item=message.get("item"),
        identifier=message.get("identifier"),
        zone=message.get("zone"),
        owner=message.get("owner"),
        ttl=message.get("ttl"),
        rtype=message.get("rtype"),
        data=message.get("data"),
        flags=message.get("flags"),
        filter_=message.get("filter"),
    )
