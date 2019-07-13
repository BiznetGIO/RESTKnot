from app.models import model
from app.libs import utils
from time import sleep


def insert_config_zone(data_zone):
    json_data = {
        "command-set": {
                "sendblock": {
                "cmd": "conf-set",
                "item": "domain", 
                "section":"zone",
                "data": data_zone['nm_zone']
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def master_create_json(data_zone, nm_master):    
    json_data = {
        "slave-set-master": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
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

def create_json_notify(data_zone, nm_master):
    json_data = {
        "slave-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
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

def create_json_acl(data_zone, nm_master):
    json_data = {
        "slave-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
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
