import yaml
import os

from app.models import model
from app.helpers import producer


def get_other_data(record_id):
    try:
        record = model.get_by_condition(table="record", field="id", value=record_id)

        zone_id = record[0]["zone_id"]
        type_id = record[0]["type_id"]
        ttl_id = record[0]["ttl_id"]

        zone = model.get_by_condition(table="zone", field="id", value=zone_id)
        type_ = model.get_by_condition(table="type", field="id", value=type_id)
        ttl = model.get_by_condition(table="ttl", field="id", value=ttl_id)
        rdata = model.get_by_condition(
            table="rdata", field="record_id", value=record_id
        )
        return (record, zone, type_, ttl, rdata)
    except Exception as e:
        raise e


def generate_command(**kwargs):

    zone_id = kwargs.get("zone_id")
    zone_name = kwargs.get("zone_name")
    owner = kwargs.get("owner")
    rtype = kwargs.get("rtype")
    ttl = kwargs.get("ttl")
    rdata = kwargs.get("rdata")
    command = kwargs.get("command")

    cmd = {
        zone_name: {
            "id_zone": zone_id,
            "type": "general",
            "command": "zone",
            "general": {
                "sendblock": {
                    "cmd": command,
                    "zone": zone_name,
                    "owner": owner,
                    "rtype": rtype,
                    "ttl": ttl,
                    "data": rdata,
                },
                "receive": {"type": "block"},
            },
        }
    }
    return cmd


def send_config(zone, zone_id, command):
    cmd = {
        zone: {
            "id_zone": zone_id,
            "type": "general",
            "command": "config",
            "general": {
                "sendblock": {
                    "cmd": command,
                    "section": "zone",
                    "item": "domain",
                    "data": zone,
                },
                "receive": {"type": "block"},
            },
        }
    }
    producer.send(cmd)


def send_zone(record_id, command):
    record, zone, type_, ttl, rdata = get_other_data(record_id)
    zone_id = zone[0]["id"]
    zone_name = zone[0]["zone"]

    cmd = generate_command(
        zone_id=zone_id,
        zone_name=zone_name,
        owner=record[0]["owner"],
        rtype=type_[0]["type"],
        ttl=ttl[0]["ttl"],
        rdata=rdata[0]["rdata"],
        command=command,
    )
    producer.send(cmd)


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


def send_cluster(zone_id):
    zone = model.get_by_condition(table="zone", field="id", value=zone_id)

    zone_id = zone[0]["id"]
    zone_name = zone[0]["zone"]
    zone_tld = zone_name.split(".")[-1]
    filename = f"{zone_name}_{zone_id}.{zone_tld}.zone"

    data = "test"  # FIXME

    clusters = get_clusters()
    master = clusters["master"]
    slave = clusters["slave"]

    command = {
        zone_name: {
            "id_zone": zone_id,
            "type": "cluster",
            "cluster": {
                "master": {
                    "file": filename,
                    "data": data,
                    "master": master["master"],
                    "notify": master["notify"],
                    "acl": master["acl"],
                    "serial-policy": "dateserial",
                    "module": "mod-stats/default",
                },
                "slave": {
                    "file": filename,
                    "master": slave["master"],
                    "acl": slave["acl"],
                    "serial-policy": "dateserial",
                    "module": "mod-stats/default",
                },
            },
        }
    }

    producer.send(command)
