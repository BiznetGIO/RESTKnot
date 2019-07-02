from app.models import model
from app import db
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

def master_create_json_master(id_zone, nm_config):
    nm_config_set = None
    if nm_config == "jkt":
        nm_config_set = "cmg"
    elif nm_config == "cmg" :
        nm_config_set = "jkt"
    else:
        print("CONFIG NOT FOUND")
    
    data_master = model.get_by_id("cs_master", "nm_config", nm_config_set)
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    data_master_set = ""
    for i in data_master:
        if data_master_set == "":
            data_master_set = i['nm_master']
        else:
            data_master_set = data_master_set+" "+i['nm_master']
    json_data = {
        "master-set-master": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "master", 
                "owner": "",
                "rtype": "",
                "ttl": "",
                "flags": "",
                "section": "zone",
                "data": data_master_set
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def master_create_json_notify(id_zone, nm_config):
    master_to_slave = None
    if nm_config == "jkt":
        master_to_slave = "cmg"
    elif nm_config == "cmg" :
        master_to_slave = "jkt"
    else:
        print("CONFIG NOT FOUND")
    master_to_slave = model.get_by_id("cs_master", "nm_config", master_to_slave)[0]['nm_master']
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    data_slave_set = ""
    # data_slave_set_jkt = ""
    for i in data_slave:
        rows = model.get_by_id("v_cs_slave_node", "not nm_config", nm_config)
        for a in rows:
            if data_slave_set == "":
                data_slave_set = a['nm_master']
            else:    
                data_slave_set = data_slave_set+" "+a['nm_master']
        if data_slave_set == "":
            data_slave_set = i['nm_slave_node']
        else:    
            data_slave_set = data_slave_set+" "+i['nm_slave_node']
    json_data = {
        "master-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "notify", 
                "owner": "",
                "rtype": "",
                "ttl": "",
                "flags": "",
                "section":"zone",
                "data": data_slave_set
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def master_create_json_acl(id_zone, nm_config):
    master_to_slave = None
    if nm_config == "jkt":
        master_to_slave = "cmg"
    elif nm_config == "cmg" :
        master_to_slave = "jkt"
    else:
        print("CONFIG NOT FOUND")
    master_to_slave = model.get_by_id("cs_master", "nm_config", master_to_slave)[0]['nm_master']
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    data_slave_set = ""
    # data_slave_set_jkt = ""
    for i in data_slave:
        rows = model.get_by_id("v_cs_slave_node", "not nm_config", nm_config)
        for a in rows:
            if data_slave_set == "":
                data_slave_set = a['nm_master']
            else:    
                data_slave_set = data_slave_set+" "+a['nm_master']
        if data_slave_set == "":
            data_slave_set = i['nm_slave_node']
        else:    
            data_slave_set = data_slave_set+" "+i['nm_slave_node']
    json_data = {
        "master-set-notify": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "acl", 
                "owner": "",
                "rtype": "",
                "ttl": "",
                "flags": "",
                "section":"zone",
                "data": data_slave_set
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def set_file_all(id_zone):
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    json_data = {
        "file-set": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "file", 
                "owner": "",
                "rtype": "",
                "ttl": "",
                "identifier": data_zone['nm_zone'],
                "section":"zone",
                "data": data_zone['nm_zone']+".zone" 
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def set_mods_stats_all(id_zone, value):
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    json_data = {
        "modstat-set": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "module", 
                "owner": "",
                "rtype": "",
                "ttl": "",
                "flags": "",
                "section":"zone",
                "data": value
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data

def set_serial_policy_all(id_zone, value):
    data_zone = model.get_by_id("zn_zone", "id_zone", id_zone)[0]
    json_data = {
        "serial-set": {
                "sendblock": {
                "cmd": "conf-set",
                "zone": data_zone['nm_zone'],
                "item": "serial-policy", 
                "owner": "",
                "rtype": "",
                "ttl": "",
                "flags": "",
                "section":"zone",
                "data": value
            },
                "receive": {
                "type": "block"
            }
        }
    }
    return json_data