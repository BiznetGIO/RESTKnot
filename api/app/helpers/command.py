from app.models import model
from app.helpers import producer

def config_zone(zone, zone_key):
    json_command = {
        zone: {
            "id_zone": zone_key,
            "type": "general",
            "command": "config",
            "general": {
                "sendblock": {
                    "cmd": "conf-set",
                    "section": "zone",
                    "item": "domain",
                    "data": zone
                },
                "receive": {
                    "type": "block"
                }
            }
        }
    }
    return json_command


def soa_default_command(soa_record_key):
    try:
        data_record = model.read_by_id("record", soa_record_key)
    except Exception as e:
        raise e
    
    try:
        zone = model.read_by_id("zone", data_record['zone'])
    except Exception as e:
        raise e

    try:
        data_type = model.read_by_id("type", data_record['type'])['value']
    except Exception as e:
        raise e
        
    if data_type != "SOA":
        return False

    try:
        data_ttl = model.read_by_id("ttl", data_record['ttl'])['value']
    except Exception as e:
        raise e
    try:
        data_content = model.content_by_record(data_record['key'])[0]['value']
    except Exception as e:
        raise e

    json_command = {
        zone['value']: {
            "id_zone": zone['key'],
            "command": "zone",
            "type": "general",
            "general": {
                    "sendblock": {
                    "cmd": "zone-set",
                    "zone": zone['value'],
                    "owner": data_record['value'],
                    "rtype": "SOA",
                    "ttl": data_ttl,
                    "data": data_content
                },
                "receive": {
                    "type": "block"
                }
            }
        }
    }
    producer.send(json_command)

def ns_default_command(record_ns_key_default):
    try:
        data_record = model.read_by_id("record", record_ns_key_default)
    except Exception as e:
        raise e
    else:
        zone = model.read_by_id("zone", str(data_record['zone']))
        ttl = model.read_by_id("ttl", str(data_record['ttl']))['value']
        types = model.read_by_id("type", str(data_record['type']))['value']
        data_content = model.content_by_record(data_record['key'])
        for i in data_content:
            json_command = {
                zone['value']: {
                    "id_zone": zone['key'],
                    "type": "general",
                    "command": "zone",
                    "general": {
                            "sendblock": {
                            "cmd": "zone-set",
                            "zone": zone['value'],
                            "owner": data_record['value'],
                            "rtype": types,
                            "ttl": ttl,
                            "data": i['value']
                        },
                        "receive": {
                            "type": "block"
                        }
                    }
                }
            }
            producer.send(json_command)

def record_insert(key):
    try:
        data_record = model.read_by_id("record", key)
    except Exception as e:
        raise e

    zone = model.read_by_id("zone", str(data_record['zone']))
    ttl = model.read_by_id("ttl", str(data_record['ttl']))['value']
    types = model.read_by_id("type", str(data_record['type']))['value']
    data_content = model.content_by_record(data_record['key'])[0]['value']
    serial = ""
    if data_record['serial']:
        serial_data = model.serial_by_record(data_record['key'])
        for i in serial_data:
            if serial == "":
                serial = i['value']
            else:
                serial = serial+" "+i['value']
        json_command = {
            zone['value']: {
                "id_zone": zone['key'],
                "command": "zone",
                "type": "general",
                "general": {
                        "sendblock": {
                        "cmd": "zone-set",
                        "zone": zone['value'],
                        "owner": data_record['value'],
                        "rtype": types,
                        "ttl": ttl,
                        "data": serial+" "+data_content
                    },
                    "receive": {
                        "type": "block"
                    }
                }
            }
        }
    else:
        json_command = {
            zone['value']: {
                "id_zone": zone['key'],
                "type": "general",
                "command": "zone",
                "general": {
                        "sendblock": {
                        "cmd": "zone-set",
                        "zone": zone['value'],
                        "owner": data_record['value'],
                        "rtype": types,
                        "ttl": ttl,
                        "data": data_content
                    },
                    "receive": {
                        "type": "block"
                    }
                }
            }
        }
        
    return json_command
        
