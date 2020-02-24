from dnsagent.libs import control
from dnsagent.libs import utils


def execute(message):
    cmd = message.get("cmd")
    zone = message.get("zone")
    item = message.get("item")
    data = message.get("data")

    response = control.send_block(
        cmd=cmd,
        section=message.get("section"),
        item=item,
        identifier=message.get("identifier"),
        zone=zone,
        owner=message.get("owner"),
        ttl=message.get("ttl"),
        rtype=message.get("rtype"),
        data=data,
        flags=message.get("flags"),
        filter_=message.get("filter"),
    )

    if response:
        utils.log_err(f"Failed: {response}")

    utils.log_info(f"Created: {cmd} {zone or ''} {item or ''} {data or ''}")
