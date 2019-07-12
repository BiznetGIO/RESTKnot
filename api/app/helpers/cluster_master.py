from app.models import model
from app import db
from app.libs import utils


def insert_config_zone(data_zone, nm_config):
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

def master_create_json_master(data_zone, nm_config):
    nm_config_set = None
    if nm_config == "jkt":
        nm_config_set = "cmg"
    elif nm_config == "cmg" :
        nm_config_set = "jkt"
    else:
        print("CONFIG NOT FOUND")
    data_master_set = ""
    try:
        data_master = model.get_by_id("cs_master", "nm_config", nm_config_set)
    except Exception as e:
        return str(e)
    else:
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

def master_create_json_notify(data_zone, nm_config, urls):
    master_to_slave = None
    if nm_config == "jkt":
        master_to_slave = "cmg"
    elif nm_config == "cmg" :
        master_to_slave = "jkt"
    else:
        print("CONFIG NOT FOUND")
    try:
        master_to_slave = model.get_by_id("cs_master", "nm_config", master_to_slave)[0]['nm_master']
        data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    except Exception as e:
        return str(e)
    else:
        data_slave_set = []
        for i in data_slave:
            try:
                rows = model.get_by_id("v_cs_slave_node", "not nm_config", nm_config)
            except Exception as e:
                return str(e)
            for a in rows:
                data_slave_set.append(a['nm_master']) 
            data_slave_set.append(i['nm_slave_node'])
        result = []
        for a in data_slave_set:
            json_data = {
                "master-set-notify": {
                    "sendblock": {
                        "cmd": "conf-set",
                        "zone": data_zone['nm_zone'],
                        "item": "notify",
                        "section":"zone",
                        "data": a
                    },
                    "receive": {
                        "type": "block"
                    }
                }
            }
            http_response = utils.send_http(urls, json_data)
            result.append(http_response)
        return result

def master_create_json_acl(data_zone, nm_config, urls):
    master_to_slave = None
    if nm_config == "jkt":
        master_to_slave = "cmg"
    elif nm_config == "cmg" :
        master_to_slave = "jkt"
    else:
        print("CONFIG NOT FOUND")

    try:
        master_to_slave = model.get_by_id("cs_master", "nm_config", master_to_slave)[0]['nm_master']
        data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    except Exception as e:
        return str(e)
    else:
        data_slave_set = []
        for i in data_slave:
            try:
                rows = model.get_by_id("cs_master", "not nm_config", nm_config)
            except Exception as e:
                return str(e)
            for a in rows:
                data_slave_set.append(a['nm_master']) 
            data_slave_set.append(i['nm_slave_node'])
        result = []
        for a in data_slave_set:
            json_data = {
                "master-set-acl": {
                    "sendblock": {
                        "cmd": "conf-set",
                        "zone": data_zone['nm_zone'],
                        "item": "acl",
                        "section":"zone",
                        "data": a
                    },
                    "receive": {
                        "type": "block"
                    }
                }
            }
            http_response = utils.send_http(urls, json_data)
            result.append(http_response)
        return result

def set_file_all(data_zone):
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

def set_mods_stats_all(data_zone, value):
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

def set_serial_policy_all(data_zone, value):
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