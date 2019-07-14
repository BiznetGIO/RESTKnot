from app.models import model
from app import db, cs_storage
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
        if cs_storage == 'static':
            data_master_yml = utils.repomaster()
            for r_master in data_master_yml:
                if r_master['nm_config'] == nm_config_set:
                    data_master = [r_master]
        else:
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
    data_slave = list()
    try:
        if cs_storage == 'static':
            data_slave_yml = utils.reposlave()
            for r_slave in data_slave_yml:
                if r_slave['nm_config'] == nm_config:
                    data_slave.append(r_slave)
        else:
            data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    except Exception as e:
        return str(e)
    else:
        data_slave_set = []
        rows = list()
        for i in data_slave:
            try:
                if cs_storage == 'static':
                    rows_yml = utils.reposlave()
                    for r_get_slave in rows_yml:
                        if r_get_slave['nm_config'] != nm_config:
                            rows.append(r_get_slave)
                else:
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
    data_slave = list()
    try:
        if cs_storage == 'static':
            data_slave_yml = utils.reposlave()
            for r_slave in data_slave_yml:
                if r_slave['nm_config'] == nm_config:
                    data_slave.append(r_slave)
        else:
            data_slave = model.get_by_id("v_cs_slave_node", "nm_config", nm_config)
    except Exception as e:
        return str(e)
    else:
        data_slave_set = []
        rows = list()
        for i in data_slave:
            try:
                if cs_storage == 'static':
                    rows_yml = utils.reposlave()
                    for r_get_slave in rows_yml:
                        if r_get_slave['nm_config'] != nm_config:
                            rows.append(r_get_slave)
                else:
                    rows = model.get_by_id("v_cs_slave_node", "not nm_config", nm_config)
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
                "data": data_zone['nm_zone']+"_"+str(data_zone['id_zone'])+".zone" 
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