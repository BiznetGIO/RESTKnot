from app.models import model
from app.helpers import producer


def config_zone(zone, zone_id):
    command = {
        zone: {
            "id_zone": zone_id,
            "type": "general",
            "command": "config",
            "general": {
                "sendblock": {
                    "cmd": "conf-set",
                    "section": "zone",
                    "item": "domain",
                    "data": zone,
                },
                "receive": {"type": "block"},
            },
        }
    }
    producer.send(command)


def get_other_data(record_id):
    try:
        record = model.get_by_id(table="record", field="id", id_=record_id)

        zone_id = record[0]["zone_id"]
        type_id = record[0]["type_id"]
        ttl_id = record[0]["ttl_id"]

        zone = model.get_by_id(table="zone", field="id", id_=zone_id)
        type_ = model.get_by_id(table="type", field="id", id_=type_id)
        ttl = model.get_by_id(table="ttl", field="id", id_=ttl_id)
        content = model.get_by_id(table="content", field="record_id", id_=record_id)
        return (record, zone, type_, ttl, content)
    except Exception as e:
        raise e


def generate_command(**kwargs):

    zone_id = kwargs.get("zone_id")
    zone_name = kwargs.get("zone_name")
    owner = kwargs.get("owner")
    rtype = kwargs.get("rtype")
    ttl = kwargs.get("ttl")
    data = kwargs.get("data")

    command = {
        zone_name: {
            "id_zone": zone_id,
            "type": "general",
            "command": "zone",
            "general": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": zone_name,
                    "owner": owner,
                    "rtype": rtype,
                    "ttl": ttl,
                    "data": data,
                },
                "receive": {"type": "block"},
            },
        }
    }
    return command


def soa_default_command(soa_record_id):
    record, zone, type_, ttl, content = get_other_data(soa_record_id)
    if type_[0]["type"] != "SOA":
        return False

    zone_id = zone[0]["id"]
    zone_name = zone[0]["zone"]

    command = generate_command(
        zone_id=zone_id,
        zone_name=zone_name,
        owner=record[0]["record"],
        rtype=type_[0]["type"],
        ttl=ttl[0]["ttl"],
        data=content[0]["content"],
    )
    producer.send(command)


def ns_default_command(ns_record_id):
    record, zone, type_, ttl, content = get_other_data(ns_record_id)
    zone_id = zone[0]["id"]
    zone_name = zone[0]["zone"]

    for i in content:
        command = generate_command(
            zone_id=zone_id,
            zone_name=zone_name,
            owner=record[0]["record"],
            rtype=type_[0]["type"],
            ttl=ttl[0]["ttl"],
            data=i["content"],
        )
        producer.send(command)


def record_insert(record_id):
    record, zone, type_, ttl, content = get_other_data(record_id)

    zone_id = zone[0]["id"]
    zone_name = zone[0]["zone"]

    serial = ""
    if record[0]["is_serial"]:
        # FIXME serial db never contain data
        serial_data = model.get_by_id(
            table="serial", field="record_id", id_=record[0]["id"]
        )

        for i in serial_data:
            if serial == "":
                serial = i["serial"]
            else:
                serial = serial + " " + i["serial"]

        command = generate_command(
            zone_id=zone_id,
            zone_name=zone_name,
            owner=record[0]["record"],
            rtype=type_[0]["type"],
            ttl=ttl[0]["ttl"],
            data=serial + " " + content[0]["content"],
        )
    else:
        command = generate_command(
            zone_id=zone_id,
            zone_name=zone_name,
            owner=record[0]["record"],
            rtype=type_[0]["type"],
            ttl=ttl[0]["ttl"],
            data=content[0]["content"],
        )

    producer.send(command)
