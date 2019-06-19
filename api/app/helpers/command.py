from app.libs import utils
from app.models import model as model
from app import db
from app.libs import utils, counter


def z_begin(url,tags):
    domain_name = None
    fields = tags['id_zone']
    domain_data = model.get_by_id("zn_zone", "id_zone", fields)
    for i in domain_data:
        domain_name = i['nm_zone']
    json_command={
        "zone-begin": {
            "sendblock": {
                "cmd": "zone-begin",
                "zone": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return utils.send_http(url,json_command)
    # return json_command

def z_commit(url,tags):
    domain_name = None
    fields = tags['id_zone']
    domain_data = model.get_by_id("zn_zone", "id_zone", fields)
    for i in domain_data:
        domain_name = i['nm_zone']

    json_command={
        "zone-commit": {
            "sendblock": {
                "cmd": "zone-commit",
                "zone": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return utils.send_http(url,json_command)

def config_insert(tags):
    fields = str(list(tags.keys())[0])
    domain_data = model.get_by_id("zn_zone", fields, tags[fields])
    domain_name = ""
    domain_id = ""
    
    for i in domain_data:
        domain_name = i['nm_zone']
        domain_id = i['id_zone']
    
    json_command = {
        "conf-set": {
            "sendblock": {
                "cmd": "conf-set",
                "section": "zone",
                "item": "domain",
                "data": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def zone_read(tags):
    domain_name = None
    fields = str(list(tags.keys())[0])
    domain_data = model.get_by_id("zn_zone", fields, tags[fields])
    for i in domain_data:
        domain_name = i['nm_zone']
    json_command={
        "zone-read": {
            "sendblock": {
                "cmd": "zone-read",
                "zone": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }

    return json_command

def conf_read():
    json_command={
        "zone-read": {
            "sendblock": {
                "cmd": "conf-read"
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command


def conf_begin_http(url):
    json_command={
        "conf-begin": {
            "sendblock": {
                "cmd": "conf-begin"
            },
            "receive": {
                "type": "block"
            }
        }
    }
    utils.send_http(url, json_command)


def conf_commit_http(url):
    json_command={
        "conf-begin": {
            "sendblock": {
                "cmd": "conf-commit"
            },
            "receive": {
                "type": "block"
            }
        }
    }
    utils.send_http(url, json_command)


def zone_soa_insert_default(tags):
    # Get Zone
    fields = str(list(tags.keys())[0])
    record = list()
    column_record = model.get_columns("v_record")
    query = "select * from v_record where "+fields+"='"+tags[fields]+"' AND nm_type='SOA'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))

    column_ttl = model.get_columns("v_ttldata")
    query = "select * from v_ttldata where "+fields+"='"+tags[fields]+"' AND nm_type='SOA'"
    db.execute(query)
    rows = db.fetchall()
    ttldata = list()
    for row in rows:
        ttldata.append(dict(zip(column_ttl, row)))
    
    content_data = list()
    column_cdata= model.get_columns("v_contentdata")
    query = "select * from v_contentdata where "+fields+"='"+tags[fields]+"' AND nm_type='SOA'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_data.append(dict(zip(column_cdata, row)))

    content_serial = list()
    column_cserial= model.get_columns("v_content_serial")
    query = "select * from v_content_serial where "+fields+"='"+tags[fields]+"' AND nm_type='SOA'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_serial.append(dict(zip(column_cserial, row)))
    
    serial_data = ""
    data = ""
    counter = str(record[0]['counter'])
    date_t = record[0]['date_record']+counter.zfill(2)

    for ns in content_data:
        data = data+" "+ns['nm_content']
    data_ns_soa = data

    for serial in content_serial:
        serial_data = serial_data+" "+serial['nm_content_serial']
    data_ns_serial = serial_data
    json_command={
        "soa-set": {
            "sendblock": {
                "cmd": "zone-set",
                "zone": record[0]['nm_zone'],
                "owner": record[0]['nm_record'],
                "rtype": "SOA",
                "ttl": ttldata[0]['nm_ttl'],
                "data": data_ns_soa+" "+date_t+" "+data_ns_serial
            },
            "receive": {
                "type": "command"
            }
        }
    }
    return record[0]['id_record'], json_command

def zone_begin(tags):
    domain_name = None
    fields = str(list(tags.keys())[0])
    domain_data = model.get_by_id("zn_zone", fields, tags[fields])
    for i in domain_data:
        domain_name = i['nm_zone']
    json_command={
        "zone-begin": {
            "sendblock": {
                "cmd": "zone-begin",
                "zone": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def zone_begin_http(url, tags):
    fields = tags['id_record']
    domain_data = model.get_by_id("v_record", "id_record", fields)
    json_command={
        "zone-begin": {
            "sendblock": {
                "cmd": "zone-begin",
                "zone": domain_data[0]['nm_zone']
            },
            "receive": {
                "type": "block"
            }
        }
    }
    
    res = utils.send_http(url, json_command)
    return res

def zone_commit_http(url, tags):
    fields = tags['id_record']
    domain_data = model.get_by_id("v_record", "id_record", fields)
    json_command={
        "zone-commit": {
            "sendblock": {
                "cmd": "zone-commit",
                "zone": domain_data[0]['nm_zone']
            },
            "receive": {
                "type": "block"
            }
        }
    }
    res = utils.send_http(url, json_command)
    return res

def zone_commit(tags):
    domain_name = None
    fields = str(list(tags.keys())[0])
    domain_data = model.get_by_id("zn_zone", fields, tags[fields])
    for i in domain_data:
        domain_name = i['nm_zone']

    json_command={
        "zone-commit": {
            "sendblock": {
                "cmd": "zone-commit",
                "zone": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def zone_insert(tags):
    # Get Record Data
    id_record = tags['id_record']
    record = list()
    column_record = model.get_columns("v_record")
    query = "select * from v_record where id_record='"+id_record+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))
    
    ttldata = list()
    column_ttldata = model.get_columns("v_ttldata")
    query = "select * from v_ttldata where id_record='"+str(record[0]['id_record'])+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        ttldata.append(dict(zip(column_ttldata, row)))
    
    ctdata = list()
    column_ctdata = model.get_columns("v_contentdata")
    query = "select * from v_contentdata where id_record='"+str(record[0]['id_record'])+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        ctdata.append(dict(zip(column_ctdata, row)))

    if record[0]['nm_type'] == "TXT":
        json_command={
            "zone-set": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": record[0]['nm_zone'],
                    "owner": record[0]['nm_record'],
                    "rtype": record[0]['nm_type'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "data": '"'+ctdata[0]['nm_content']+'"'
                },
                "receive": {
                    "type": "block"
                }
            }
        }
    elif record[0]['nm_type'] == "A":
        check_valid = utils.a_record_validation(ctdata[0]['nm_content'])
        if check_valid:
            json_command={
                "zone-set": {
                    "sendblock": {
                        "cmd": "zone-set",
                        "zone": record[0]['nm_zone'],
                        "owner": record[0]['nm_record'],
                        "rtype": record[0]['nm_type'],
                        "ttl": ttldata[0]['nm_ttl'],
                        "data": ctdata[0]['nm_content']
                    },
                    "receive": {
                        "type": "block"
                    }
                }
            }
    else:   
        json_command={
            "zone-set": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": record[0]['nm_zone'],
                    "owner": record[0]['nm_record'],
                    "rtype": record[0]['nm_type'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "data": ctdata[0]['nm_content']
                },
                "receive": {
                    "type": "block"
                }
            }
        }
    counter.update_counter(record[0]['nm_zone'])
    return json_command

def zone_ns_insert(tags):
    fields = str(list(tags.keys())[0])
    record = list()
    column_record = model.get_columns("v_record")
    query = "select * from v_record where "+fields+"='"+tags[fields]+"' AND nm_type='NS'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))

    ttldata = list()
    column_ttldata = model.get_columns("v_ttldata")
    query = "select * from v_ttldata where id_record='"+str(record[0]['id_record'])+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        ttldata.append(dict(zip(column_ttldata, row)))

    ctdata = list()
    column_ctdata = model.get_columns("v_contentdata")
    query = "select * from v_contentdata where id_record='"+str(record[0]['id_record'])+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        ctdata.append(dict(zip(column_ctdata, row)))
    command_ns = list()
    for ctn in ctdata:
        json_command={
            "zone-set": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": record[0]['nm_zone'],
                    "owner": "@",
                    "rtype": record[0]['nm_type'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "data": ctn['nm_content']
                },
                "receive": {
                    "type": "block"
                }
            }
        }
        command_ns.append({
            "id_record": record[0]['id_record'],
            "command": json_command
        })
    counter.update_counter(record[0]['nm_zone'])
    return command_ns

def zone_insert_srv(tags):
    # Get Zone
    fields = tags['id_record']
    record = list()
    column_record = model.get_columns("v_record")
    query = "select * from v_record where id_record='"+fields+"' AND nm_type='SRV'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))

    column_ttl = model.get_columns("v_ttldata")
    query = "select * from v_ttldata where id_record='"+fields+"' AND nm_type='SRV'"
    db.execute(query)
    rows = db.fetchall()
    ttldata = list()
    for row in rows:
        ttldata.append(dict(zip(column_ttl, row)))
    
    content_data = list()
    column_cdata= model.get_columns("v_contentdata")
    query = "select * from v_contentdata where id_record='"+fields+"' AND nm_type='SRV'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_data.append(dict(zip(column_cdata, row)))

    content_serial = list()
    column_cserial= model.get_columns("v_content_serial")
    query = "select * from v_content_serial where id_record='"+fields+"' AND nm_type='SRV'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_serial.append(dict(zip(column_cserial, row)))
    
    serial_data = ""
    data = ""
    for ns in content_data:
        data = data+" "+ns['nm_content']
    for serial in content_serial:
        serial_data = serial_data+" "+serial['nm_content_serial']
    data_ns_soa = data
    data_ns_serial = serial_data

    
    json_command = {
                    "srv-set": {
                        "sendblock": {
                            "cmd": "zone-set",
                            "zone": record[0]['nm_zone'],
                            "owner": record[0]['nm_record'],
                            "rtype": record[0]['nm_type'],
                            "ttl": ttldata[0]['nm_ttl'],
                            "data": data_ns_soa+""+data_ns_serial
                        },
                        "receive": {
                            "type": "command"
                        }
                    }
                }
    counter.update_counter(record[0]['nm_zone'])
    return json_command

def zone_insert_mx(tags):
    # Get Zone
    fields = tags['id_record']
    record = list()
    column_record = model.get_columns("v_record")
    query = "select * from v_record where id_record='"+fields+"' AND nm_type='MX'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))
    column_ttl = model.get_columns("v_ttldata")
    query = "select * from v_ttldata where id_record='"+fields+"' AND nm_type='MX'"
    db.execute(query)
    rows = db.fetchall()
    ttldata = list()
    for row in rows:
        ttldata.append(dict(zip(column_ttl, row)))
    
    content_data = list()
    column_cdata= model.get_columns("v_contentdata")
    query = "select * from v_contentdata where id_record='"+fields+"' AND nm_type='MX'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_data.append(dict(zip(column_cdata, row)))

    content_serial = list()
    column_cserial= model.get_columns("v_content_serial")
    query = "select * from v_content_serial where id_record='"+fields+"' AND nm_type='MX'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_serial.append(dict(zip(column_cserial, row)))
    
    serial_data = ""
    data = ""
    for ns in content_data:
        data = data+" "+ns['nm_content']
    for serial in content_serial:
        serial_data = serial_data+" "+serial['nm_content_serial']
    data_ns_soa = data
    data_ns_serial = serial_data

    json_command = {
                    "mx-set": {
                        "sendblock": {
                            "cmd": "zone-set",
                            "zone": record[0]['nm_zone'],
                            "owner": record[0]['nm_record'],
                            "rtype": record[0]['nm_type'],
                            "ttl": ttldata[0]['nm_ttl'],
                            "data": data_ns_soa+""+data_ns_serial
                        },
                        "receive": {
                            "type": "command"
                        }
                    }
                }
    return json_command


def conf_unset(tags):
    id_zone = tags['id_zone']
    record = list()
    column_record = model.get_columns("zn_zone")
    query = "select * from zn_zone where id_zone='"+id_zone+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))
    json_command={
        "conf-unset": {
            "sendblock": {
                "cmd": "conf-unset",
                "section": "zone",
                "item": "domain",
                "data":record[0]['nm_zone']
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def conf_purge(tags):
    id_zone = tags['id_zone']
    record = list()
    column_record = model.get_columns("zn_zone")
    query = "select * from zn_zone where id_zone='"+id_zone+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))
    json_command={
        "zone-purge": {
            "sendblock": {
                "cmd": "zone-purge",
                "zone": record[0]['nm_zone'],
                "owner": record[0]['nm_zone']
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def zone_unset(tags):
    json_command = None
    id_record = tags['id_record']
    record = list()
    column_record = model.get_columns("v_record")
    query = "select * from v_record where id_record='"+id_record+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))

    ttldata = list()
    column_ttldata = model.get_columns("v_ttldata")
    query = "select * from v_ttldata where id_record='"+str(record[0]['id_record'])+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        ttldata.append(dict(zip(column_ttldata, row)))

    ctdata = list()
    column_ctdata = model.get_columns("v_contentdata")
    query = "select * from v_contentdata where id_record='"+str(record[0]['id_record'])+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        ctdata.append(dict(zip(column_ctdata, row)))
    content_data = ""
    for ct in ctdata:
        content_data = content_data+ct['nm_content']

    content_serial = list()
    column_cserial= model.get_columns("v_content_serial")
    query = "select * from v_content_serial where id_record='"+str(record[0]['id_record'])+"' AND nm_type='"+record[0]['nm_type']+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        content_serial.append(dict(zip(column_cserial, row)))
    serial_data = ""
    if content_serial:
        for serial in content_serial:
            serial_data = serial_data+serial['nm_content_serial']

    json_command={
        "zone-unset": {
            "sendblock": {
                "cmd": "zone-unset",
                "zone": record[0]['nm_zone'],
                "owner": record[0]['nm_record'],
                "ttl": ttldata[0]['nm_ttl'],
                "rtype": record[0]['nm_type'],
                "data": content_data+" "+serial_data
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def conf_set_notify_master(tags):
    # Get Zone
    fields = tags['id_zone']
    record = list()
    record_slave = list()
    column_record_master = model.get_columns("v_cs_notify_master")
    query_master = "select * from v_cs_notify_master where id_zone='"+fields+"'"
    db.execute(query_master)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record_master, row)))

    column_record_slave = model.get_columns("v_cs_notify_slave")
    query_slave = "select * from v_cs_notify_slave where id_zone='"+fields+"'"
    db.execute(query_slave)
    rows_slave = db.fetchall()
    for rw in rows_slave:
        record_slave.append(dict(zip(column_record_slave, rw)))
    # data = ""
    # for i in record_slave:
    #     data = data+" '"+i['nm_slave']+"'"
    json_command = list()

    for keys in record_slave:
        json_data = {
            "cluster-set": {
                "sendblock": {
                    "cmd": "conf-set",
                    "zone": keys['nm_zone'],
                    "rtype": 'notify',
                    "owner": 'master',
                    "ttl":'',
                    "data": keys['nm_master']
                },
                "receive": {
                    "type": "command",
                    "master": keys['nm_master'],
                    "uri": keys['ip_slave'],
                    "port": keys['slave_port'],
                    "id_notify_master": keys['id_notify_master']
                }
            }
        }
        json_command.append(json_data)
    return json_command


def conf_set_notify_slave(tags):
    # Get Zone
    fields = tags['id_zone']
    record = list()
    record_master = list()
    column_record_slave = model.get_columns("v_cs_notify_slave")
    query_slave = "select * from v_cs_notify_slave where id_zone='"+fields+"'"
    db.execute(query_slave)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record_slave, row)))

    column_record_master = model.get_columns("v_cs_notify_master")
    query_master = "select * from v_cs_notify_master where id_zone='"+fields+"'"
    db.execute(query_master)
    rows_master = db.fetchall()
    for r_master in rows_master:
        record_master.append(dict(zip(column_record_master, r_master)))

    json_command = list()

    for keys in record:
        json_data = {
            "cluster-set": {
                "sendblock": {
                    "cmd": "conf-set",
                    "zone": keys['nm_zone'],
                    "rtype": 'notify',
                    "owner": 'slave',
                    "ttl":"",
                    "data": keys['nm_master']
                },
                "receive": {
                    "type": "command",
                    "slave": keys['nm_slave'],
                    "uri":keys['ip_slave'],
                    "port": keys['slave_port'],
                    "id_notify_slave": keys['id_notify_slave']
                }
            }
        }
        json_command.append(json_data)
    return json_command


def conf_set_acl_master(tags):
    # Get Zone
    fields = tags['id_zone']
    record = list()
    record_slave = list()
    column_record_master = model.get_columns("v_cs_acl_master")
    query_master = "select * from v_cs_acl_master where id_zone='"+fields+"'"
    db.execute(query_master)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record_master, row)))

    column_record_slave = model.get_columns("v_cs_acl_slave")
    query_slave = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
    db.execute(query_slave)
    rows_slave = db.fetchall()
    for rw in rows_slave:
        record_slave.append(dict(zip(column_record_slave, rw)))

    data = ""
    for i in record_slave:
        data = data+" '"+i['nm_slave']+"'"

    json_command = list()
    for keys in record:
        json_data = {
            "cluster-set": {
                "sendblock": {
                    "cmd": "conf-set",
                    "zone": keys['nm_zone'],
                    "rtype": 'acl',
                    "owner": 'master',
                    "ttl":'',
                    "data": data
                },
                "receive": {
                    "type": "command",
                    "master": keys['nm_master'],
                    "uri": keys['ip_master'],
                    "port": keys['port'],
                    "id_acl_master": keys['id_acl_master']
                }
            }
        }
        json_command.append(json_data)
    return json_command


def conf_set_acl_slave(tags):
    # Get Zone
    fields = tags['id_zone']
    record = list()
    record_master = list()
    column_record_slave = model.get_columns("v_cs_acl_slave")
    query_slave = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
    db.execute(query_slave)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record_slave, row)))

    data = ""
    for i in record:
        data = data+" '"+i['nm_slave']+"'"
    print(record)
    column_record_master = model.get_columns("v_cs_acl_master")
    query_master = "select * from v_cs_acl_master where id_zone='"+fields+"'"
    db.execute(query_master)
    rows_master = db.fetchall()
    for r_master in rows_master:
        record_master.append(dict(zip(column_record_master, r_master)))

    json_command = list()

    for keys in record_master:
        json_data = {
            "cluster-set": {
                "sendblock": {
                    "cmd": "conf-set",
                    "zone": keys['nm_zone'],
                    "rtype": 'notify',
                    "owner": 'master',
                    "ttl":"",
                    "data": data
                },
                "receive": {
                    "type": "command",
                    "master": keys['nm_master'],
                    "uri":keys['ip_master'],
                    "port": keys['port'],
                    "id_acl_master": keys['id_acl_master']
                }
            }
        }
        json_command.append(json_data)
    return json_command


def conf_set_file(tags):
    # Get Zone
    fields = tags['id_zone']
    record = list()
    column_record = model.get_columns("v_cs_acl_slave")
    query = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))
    json_command = list()
    for i in record:
        json_data = {
            "cluster-set": {
                "sendblock": {
                    "cmd": "conf-set",
                    "zone": i['nm_zone'],
                    "rtype": 'file',
                    "owner": 'all',
                    "ttl":'',
                    "data": ""
                },
                "receive": {
                    "type": "command",
                    "slave_uri": i['ip_slave'],
                    "master_uri": i['ip_master'],
                    "master_port": i['port_master'],
                    "slave_port": i['port_slave'],
                }
            }
        }
        json_command.append(json_data)
    return json_command


def conf_set_module(tags):
    # Get Zone
    fields = tags['id_zone']
    record = list()
    column_record = model.get_columns("v_cs_acl_slave")
    query = "select * from v_cs_acl_slave where id_zone='"+fields+"'"
    db.execute(query)
    rows = db.fetchall()
    for row in rows:
        record.append(dict(zip(column_record, row)))
    json_command = list()
    for i in record:
        json_data = {
            "cluster-set": {
                "sendblock": {
                    "cmd": "conf-set",
                    "zone": i['nm_zone'],
                    "rtype": 'module',
                    "owner": 'all',
                    "ttl":'',
                    "data": ""
                },
                "receive": {
                    "type": "command",
                    "slave_uri": i['ip_slave'],
                    "master_uri": i['ip_master'],
                    "master_port": i['port_master'],
                    "slave_port": i['port_slave'],
                }
            }
        }
        json_command.append(json_data)
    return json_command
