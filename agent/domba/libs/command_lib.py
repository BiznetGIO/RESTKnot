import os

def insert_config_zone(zone):
    json_data = {
        "command-set": {
                "sendblock": {
                "cmd": "conf-set",
                "item": "domain", 
                "section":"zone",
                "data": zone
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def create_json_notify(zone, nm_master):
    json_data = {
        "slave-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "notify", 
                "section":"zone",
                "data": nm_master
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def master_create_json(zone, nm_master):    
    json_data = {
        "slave-set-master": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "master", 
                "section": "zone",
                "data": nm_master
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data


def create_json_acl(zone, nm_master):
    json_data = {
        "slave-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "acl", 
                "section":"zone",
                "data": nm_master
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data


def set_file(zone, id_zone):
    json_data = {
        "file-set": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "file",
                "identifier": zone,
                "section":"zone",
                "data": str(id_zone)+"_"+zone+".zone" 
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def set_mods_stats(zone, value):
    json_data = {
        "modstat-set": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "module", 
                "section":"zone",
                "data": value
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def set_serial_policy(zone, value):
    json_data = {
        "serial-set": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": zone,
                "item": "serial-policy", 
                "section":"zone",
                "data": value
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data