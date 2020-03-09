import logging

from dnsagent.libs import control

logger = logging.getLogger(__name__)


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
        logger.error(f"{response}")
        logger.info(f"Fail: {response}")

    logger.info(f"Success: {cmd} {zone or ''} {item or ''} {data or ''}")
