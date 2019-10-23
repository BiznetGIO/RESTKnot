from app.models import model
from app.helpers import producer


def config_zone(zone, zone_id):
    json_command = {
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
    return json_command


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


def soa_default_command(soa_record_id):
    record, zone, type_, ttl, content = get_other_data(soa_record_id)

    type_value = type_[0]["type"]
    if type_value != "SOA":
        return False

    # FIXME duplicate code
    json_command = {
        zone[0]["zone"]: {
            "id_zone": zone[0]["id"],
            "command": "zone",
            "type": "general",
            "general": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": zone[0]["zone"],
                    "owner": record[0]["record"],
                    "rtype": "SOA",
                    "ttl": ttl[0]["ttl"],
                    "data": content[0]["content"],
                },
                "receive": {"type": "block"},
            },
        }
    }
    producer.send(json_command)


def ns_default_command(ns_record_id):
    record, zone, type_, ttl, contents = get_other_data(ns_record_id)
    for content in contents:
        json_command = {
            zone[0]["zone"]: {
                "id_zone": zone[0]["id"],
                "type": "general",
                "command": "zone",
                "general": {
                    "sendblock": {
                        "cmd": "zone-set",
                        "zone": zone[0]["zone"],
                        "owner": record[0]["record"],
                        "rtype": type_[0]["type"],
                        "ttl": ttl[0]["ttl"],
                        "data": content["content"],
                    },
                    "receive": {"type": "block"},
                },
            }
        }
        producer.send(json_command)


def record_insert(key):
    record, zone, type_, ttl, content = get_other_data(key)
    is_serial = record[0]["is_serial"]
    serial_value = ""
    serial_data = ""

    if is_serial:
        serials = model.get_by_id(table="serial", field="record_id", id_=key)
        for serial in serials:
            if serial_value == "":
                serial_value = serial["serial"]
            else:
                serial_value = serial + " " + serial["serial"]
        serial_data = f'{serial_value} {content[0]["content"]}'
    else:
        serial_data = content[0]["content"]

    json_command = {
        zone[0]["zone"]: {
            "id_zone": zone[0]["id"],
            "type": "general",
            "command": "zone",
            "general": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": zone[0]["zone"],
                    "owner": record[0]["record"],
                    "rtype": type_[0]["type"],
                    "ttl": ttl[0]["ttl"],
                    "data": serial_data,
                },
                "receive": {"type": "block"},
            },
        }
    }

    return json_command
