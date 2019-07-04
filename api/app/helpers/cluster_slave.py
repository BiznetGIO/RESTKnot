from app.models import model
from app.libs import utils


def insert_config_zone(id_zone, nm_config):
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
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

def master_create_json(id_zone, nm_config):    
    data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    data_master_set = ""
    for i in data_slave:
        if data_master_set == "":
            data_master_set = i['nm_master']
        else:
            data_master_set = data_master_set+" "+i['nm_master']
    json_data = {
        "slave-set-master": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "master", 
                "section": "zone",
                "data": data_master_set
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def create_json_notify(id_zone, nm_config, nm_slave):
    master_to_notify = model.get_by_id("cs_master", "nm_config", nm_config)[0]['nm_master']
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    data_slave_set = master_to_notify
    for i in data_slave:
        if i['nm_slave_node'] != nm_slave:
            data_slave_set = data_slave_set+" "+i['nm_slave_node']
    json_data = {
        "slave-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "notify", 
                "section":"zone",
                "data": data_slave_set
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def create_json_acl(id_zone, nm_config, nm_slave):
    master_to_notify = model.get_by_id("cs_master", "nm_config", nm_config)[0]['nm_master']
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    data_slave_set = master_to_notify
    for i in data_slave:
        if i['nm_slave_node'] != nm_slave:
            data_slave_set = data_slave_set+" "+i['nm_slave_node']
    json_data = {
        "slave-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "notify", 
                "section":"zone",
                "data": data_slave_set
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data
