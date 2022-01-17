from typing import Dict, Tuple

import json

from app.helpers import helpers, producer
from app.models import record as record_db
from app.models import rtype as rtype_db
from app.models import ttl as ttl_db
from app.models import zone as zone_db


def get_other_data(record_id: int) -> Tuple[Dict, Dict, Dict, Dict]:
    """Return other record data from given record id."""
    try:
        record = record_db.get(record_id)
        if not record:
            raise ValueError("record not found")

        zone = zone_db.get(record["zone_id"])
        if not zone:
            raise ValueError("zone not found")

        type_ = rtype_db.get(record["rtype_id"])
        if not type_:
            raise ValueError("type_ not found")

        ttl = ttl_db.get(record["ttl_id"])
        if not ttl:
            raise ValueError("ttl not found")

        return (record, zone, type_, ttl)
    except Exception as error:
        raise ValueError(f"{error}")


def generate_command(
    zone: str, owner: str, rtype: str, ttl: str, rdata: str, command: str
) -> Dict:
    """Return dictionary of given keywords & values."""
    cmd = {
        "cmd": command,
        "zone": zone,
        "owner": owner,
        "rtype": rtype,
        "ttl": ttl,
        "data": rdata,
    }

    return cmd


def set_config(zone_name: str, command: str):
    """Send config command with JSON structure to broker."""

    # there are two option to put conf-begin and conf-commit
    # either here (api) or in (agent)
    # I'd rather choose to put it here for finer tuning
    conf_begin = {"cmd": "conf-begin", "zone": zone_name}
    conf_set = {"cmd": command, "section": "zone", "item": "domain", "data": zone_name}
    conf_commit = {"cmd": "conf-commit", "zone": zone_name}

    queries = []
    for query in [conf_begin, conf_set, conf_commit]:
        queries.append(query)

    # agent_type: master, slave
    # because config created both in  master and slave
    message = {"agent": {"agent_type": ["master", "slave"]}, "knot": queries}

    producer.send(message)


def set_zone(record_id: int, command: str):
    """Send zone command with JSON structure to broker."""
    record, zone, rtype, ttl = get_other_data(record_id)
    zone_name = zone["zone"]

    # escape space and double quote in txt rdata
    rdata = record["rdata"]
    if rtype["rtype"] == "TXT":
        rdata = json.dumps(record["rdata"])

    zone_begin = {"cmd": "zone-begin", "zone": zone_name}
    zone_set = generate_command(
        zone=zone_name,
        owner=record["owner"],
        rtype=rtype["rtype"],
        ttl=ttl["ttl"],
        rdata=rdata,
        command=command,
    )
    zone_commit = {"cmd": "zone-commit", "zone": zone_name}

    queries = []
    for query in [zone_begin, zone_set, zone_commit]:
        queries.append(query)

    # agent_type: master
    # because zone only created in master, slave will get zone via axfr
    message = {"agent": {"agent_type": ["master"]}, "knot": queries}

    producer.send(message)


def delegate(zone_name: str, command: str, agent_type: str):
    """Send delegation config command with JSON structure to broker."""
    config = helpers.get_config()
    try:
        clusters = config["knot_servers"]
    except KeyError:
        raise ValueError("Can't Knot server list in config")

    cluster = clusters[agent_type]

    # default for master
    cluster_type = "notify"
    cluster_type_item = "notify"
    if agent_type == "slave":
        cluster_type = "master"
        cluster_type_item = "master"

    queries = [
        {"item": "file", "data": f"{zone_name}.zone", "identifier": zone_name},
        {"item": "serial-policy", "data": "dateserial"},
        {"item": "module", "data": "mod-stats/default"},
    ]
    queries.extend(
        [{"item": cluster_type_item, "data": item} for item in cluster[cluster_type]]
    )

    queries.extend([{"item": "acl", "data": acl} for acl in cluster["acl"]])

    queries_ = []
    for query in queries:
        query["cmd"] = command
        query["section"] = "zone"
        query["zone"] = zone_name
        queries_.append(query)

    message = {
        "agent": {"agent_type": [agent_type]},
        "knot": [{"cmd": "conf-begin"}, *queries_, {"cmd": "conf-commit"}],
    }

    producer.send(message)
