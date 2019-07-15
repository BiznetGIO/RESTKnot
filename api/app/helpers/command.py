from app.libs import utils
from app.models import model as model
from app import db
from app.libs import utils, counter


def cluster_command_new(tags, location, type):
    domain_name = None
    fields = tags['id_zone']
    domain_data = model.get_by_id("zn_zone", "id_zone", fields)
    for i in domain_data:
        domain_name = i['nm_zone']

    json_command={
        "cluster-set": {
            "sendblock": {
                "cmd": "conf-set",
                "zone": domain_name,
                "owner": "master",
                "rtype": "cluster",
                "ttl": "",
                "data": location
            },
            "receive": {
                "type": "command"
            }
        }
    }
    return json_command


def unset_cluster_command_new(tags, domain_name):
    json_command={
        "cluster-set": {
            "sendblock": {
                "cmd": "conf-unset",
                "item": "domain",
                "section":"zone",
                "data": domain_name
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

    
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
    
    for i in domain_data:
        domain_name = i['nm_zone']
    
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
        ct_data = ctdata[0]['nm_content']
        ct_data_fix = ct_data.replace('"', '\\"')
        json_command={
            "zone-set": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": record[0]['nm_zone'],
                    "owner": record[0]['nm_record'],
                    "rtype": record[0]['nm_type'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "data": '"'+ct_data_fix+'"'
                },
                "receive": {
                    "type": "block"
                }
            }
        }
        return json_command
        
    if record[0]['nm_type'] == "MX":
        ct_data = ctdata[0]['nm_content']
        cs_data = []
        cs_clm_data = model.get_columns("v_content_serial")
        query_serial = "SELECT * FROM v_content_serial where id_record='"+str(record[0]['id_record'])+"'"
        db.execute(query_serial)
        rw_serial = db.fetchall()
        for rw in rw_serial:
            cs_data.append(dict(zip(cs_clm_data, rw)))
        
        json_command={
            "zone-set": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": record[0]['nm_zone'],
                    "owner": record[0]['nm_record'],
                    "rtype": record[0]['nm_type'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "data": ct_data+' '+cs_data[0]['nm_content_serial']
                },
                "receive": {
                    "type": "block"
                }
            }
        }
        return json_command
    if record[0]['nm_type'] == "SRV":
        ct_data = ctdata[0]['nm_content']
        cs_data = []
        cs_clm_data = model.get_columns("v_content_serial")
        query_serial = "SELECT * FROM v_content_serial where id_record='"+str(record[0]['id_record'])+"'"
        db.execute(query_serial)
        rw_serial = db.fetchall()
        for rw in rw_serial:
            cs_data.append(dict(zip(cs_clm_data, rw)))
        data_ct = ""
        for ri in cs_data:
            data_ct = data_ct+" "+ri['nm_content_serial']


        json_command={
            "zone-set": {
                "sendblock": {
                    "cmd": "zone-set",
                    "zone": record[0]['nm_zone'],
                    "owner": record[0]['nm_record'],
                    "rtype": record[0]['nm_type'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "data": ct_data+' '+data_ct
                },
                "receive": {
                    "type": "block"
                }
            }
        }
        return json_command
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
    
    if serial_data != "":
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
    else:
        if record[0]['nm_type'] == 'TXT':
            # content_data_t = content_data.replace("\\",'\\')
            content_data_fix = content_data.replace('"','\\\"')
            json_command={
                "zone-unset": {
                    "sendblock": {
                        "cmd": "zone-unset",
                        "zone": record[0]['nm_zone'],
                        "owner": record[0]['nm_record'],
                        "ttl": ttldata[0]['nm_ttl'],
                        "rtype": record[0]['nm_type'],
                        "data": '"'+content_data_fix+'"'
                    },
                    "receive": {
                        "type": "block"
                    }
                }
            }
        else:
            json_command={
            "zone-unset": {
                "sendblock": {
                    "cmd": "zone-unset",
                    "zone": record[0]['nm_zone'],
                    "owner": record[0]['nm_record'],
                    "ttl": ttldata[0]['nm_ttl'],
                    "rtype": record[0]['nm_type'],
                    "data": content_data
                },
                "receive": {
                    "type": "block"
                }
            }
        }
    return json_command

    