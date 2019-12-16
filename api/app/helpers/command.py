import yaml
import os

from app.models import model
from app.helpers import producer


def get_other_data(record_id):
    try:
        record = model.get_one(table="record", field="id", value=record_id)

        zone_id = record["zone_id"]
        type_id = record["type_id"]
        ttl_id = record["ttl_id"]

        zone = model.get_one(table="zone", field="id", value=zone_id)
        type_ = model.get_one(table="type", field="id", value=type_id)
        ttl = model.get_one(table="ttl", field="id", value=ttl_id)
        rdata = model.get_one(table="rdata", field="record_id", value=record_id)
        return (record, zone, type_, ttl, rdata)
    except Exception as error:
        raise ValueError(f"{error}")


def generate_command(**kwargs):
    zone = kwargs.get("zone_name")
    owner = kwargs.get("owner")
    rtype = kwargs.get("rtype")
    ttl = kwargs.get("ttl")
    rdata = kwargs.get("rdata")
    command = kwargs.get("command")

    cmd = {
        "cmd": command,
        "zone": zone,
        "owner": owner,
        "rtype": rtype,
        "ttl": ttl,
        "data": rdata,
    }

    return cmd


def send_config(zone, zone_id, command):
    """Send config command with JSON structure to broker."""

    # there are two option to put conf-begin and conf-commit
    # either here (api) or in (agent)
    # I'd rather choose to put it here for finer tuning
    conf_begin = {"cmd": "conf-begin", "zone": zone}
    conf_set = {"cmd": command, "section": "zone", "item": "domain", "data": zone}
    conf_commit = {"cmd": "conf-commit", "zone": zone}

    for query in [conf_begin, conf_set, conf_commit]:
        producer.send(query)


def send_zone(record_id, command):
    """Send zone command with JSON structure to broker."""
    record, zone, type_, ttl, rdata = get_other_data(record_id)
    zone_name = zone["zone"]

    zone_begin = {"cmd": "zone-begin", "zone": zone_name}
    zone_set = generate_command(
        zone=zone_name,
        owner=record["owner"],
        rtype=type_["type"],
        ttl=ttl["ttl"],
        rdata=rdata["rdata"],
        command=command,
    )
    zone_commit = {"cmd": "zone-commit", "zone": zone_name}

    for query in [zone_begin, zone_set, zone_commit]:
        producer.send(query)


def cluster_file():
    path = os.environ.get("RESTKNOT_CLUSTER_FILE")
    if not path:
        raise ValueError(f"RESTKNOT_CLUSTER_FILE is not set")

    is_exists = os.path.exists(path)
    if is_exists:
        return path
    else:
        raise ValueError(f"Clustering File Not Found")


def get_clusters():
    file_ = cluster_file()
    clusters = yaml.safe_load(open(file_))
    return clusters


def send_cluster(zone, zone_id, command):
    clusters = get_clusters()
    slave = clusters["slave"]
    # master = clusters["master"]
    cmds = []

    file_cmd = {"item": "file", "data": f"{zone}.zone", "identifier": zone}
    cmds.append(file_cmd)

    # master zone
    for remote in slave["remote"]:
        master_cmd = {"item": "notify", "data": remote.get("id")}
        cmds.append(master_cmd)

    for acl in slave["acl"]:
        master_cmd = {"item": "acl", "data": acl.get("id")}
        cmds.append(master_cmd)

    # slave zone
    # for master in master["remote"]:
    #     master_cmd = {"item": "master", "data": master.get("id")}
    #     cmds.append(master_cmd)

    # for master in master["acl"]:
    #     master_cmd = {"item": "acl", "data": master.get('id')}
    #     cmds.append(master_cmd)

    serial_cmd = {"item": "serial-policy", "data": "dateserial"}
    cmds.append(serial_cmd)

    module_cmd = {"item": "module", "data": "mod-stats/default"}
    cmds.append(module_cmd)

    conf_begin = {"cmd": "conf-begin"}
    producer.send(conf_begin)

    for cmd in cmds:
        cmd["cmd"] = command
        cmd["section"] = "zone"
        cmd["zone"] = zone
        producer.send(cmd)

    conf_commit = {"cmd": "conf-commit"}
    producer.send(conf_commit)
