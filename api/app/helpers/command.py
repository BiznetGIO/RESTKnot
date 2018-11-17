from app.libs import utils
from app.models import api_models as db


def config_insert(tags):
    domain_data = db.row("domain", tags)
    domain_name = ""
    domain_id = ""

    for i in domain_data['data']:
        domain_name = i['domain_name']
        domain_id = i['domain_id']
    
    json_command = {
        "conf-begin": {
            "sendblock": {
                "cmd": "conf-begin"
            },
            "receive": {
                "type": "block"
            }
        },
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
        },
        "conf-commit": {
            "sendblock": {
                "cmd": "conf-commit"
            },
            "receive": {
                "type": "block"
            }
        }
    }
    return json_command

def zone_read(tags):
    domain_name = None
    domain_data = db.row("domain", tags)
    # try:
    #     
    # except Exception as e:
    #     print(e)
    print(domain_data)
    if domain_data['data'] == []:
        print("OK")
    
    for i in domain_data['data']:
        domain_name = i['domain_name']
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

def zone_soa_insert_default(tags):

    # Get Zone
    tags_zone = {
        "zone_id": tags['zone_id']
    }
    zone = db.row("zone", tags_zone)
    # print(zone)
    # Get Domain
    tags_domain={
        "domain_id": zone['data'][0]['domain_id']
    }
    
    domain = db.row("domain", tags_domain)

    # Get Record Data
    tags_record_data = {
        "zone_id": tags['zone_id']
    }
    record_data = db.row("datarecord", tags_record_data)
    
    # Get Record Name
    tags_type_name = {
        "type_name_id": record_data['data'][0]['type_name_id']
    }
    record = db.row("typename", tags_type_name)
    
    # Get ttl data
    tags_ttldata = {
        "ttl_data_id": tags['ttl_data_id']
    }
    ttldata = db.row("datattl",tags_ttldata)
    
    tags_ttlid = {
        "ttl_id": ttldata['data'][0]['ttl_id']
    }
    ttl = db.row("ttl",tags_ttlid)

    # Get Content
    tags_content={
        "ttl_data_id": tags['ttl_data_id']
    }
    content = db.row("content", tags_content)
    tags_content_data ={
        "content_id": tags['content_id']
    }

    content_data = db.row("datacontent", tags_content_data)
    # print(content_data)
    serial_data = ""
    data = ""

    for ns in content['data']:
        data = data+" "+ns['content_name']
    # print(data)
    data_date = content_data['data'][0]['content_data_date']
    for serial in content_data['data']:
        serial_data = serial_data+" "+serial['content_data_name']
    data_ns_soa = data
    data_ns_serial = serial_data
    json_command={
        "soa-set": {
            "sendblock": {
                "cmd": "zone-set",
                "zone": domain['data'][0]['domain_name'],
                "owner": domain['data'][0]['domain_name'],
                "rtype": "SOA",
                "ttl": ttl['data'][0]['ttl_name'],
                "data": data_ns_soa+" "+data_date+" "+data_ns_serial
            },
            "receive": {
                "type": "command"
            }
        }
    }
    return json_command

def zone_begin(tags):
    domain_data = db.row("domain", tags)
    domain_name = ""

    for i in domain_data['data']:
        domain_name = i['domain_name']

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

def zone_commit(tags):
    domain_data = db.row("domain", tags)
    domain_name = ""

    for i in domain_data['data']:
        domain_name = i['domain_name']

    json_command={
        "zone-read": {
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
    tags_record_data = {
        "record_data_id": tags['record_data_id']
    }
    record_data = db.row("datarecord", tags_record_data)
    tags_zone = {
        "zone_id": record_data['data'][0]['zone_id']
    }

    zone = db.row("zone", tags_zone)
    # Get Domain
    tags_domain={
        "domain_id": zone['data'][0]['domain_id']
    }
    domain = db.row("domain", tags_domain)

    # Get Record Name
    tags_type_name = {
        "type_name_id": record_data['data'][0]['type_name_id']
    }
    record = db.row("typename", tags_type_name)

    # Get ttl data
    tags_ttldata = {
        "ttl_data_id": tags['ttl_data_id']
    }
    ttldata = db.row("datattl",tags_ttldata)
    tags_ttlid = {
        "ttl_id": ttldata['data'][0]['ttl_id']
    }
    ttl = db.row("ttl",tags_ttlid)

    # Get Content
    tags_content={
        "ttl_data_id": tags['ttl_data_id']
    }
    content = db.row("content", tags_content)
    
    json_command={
        "zone-begin": {
                "sendblock": {
                "cmd": "zone-begin",
                "zone": zone['data'][0]['zone_name']
            },
            "receive": {
                "type": "block"
            }
        },
        "zone-set": {
            "sendblock": {
                "cmd": "zone-set",
                "zone": zone['data'][0]['zone_name'],
                "owner": record_data['data'][0]['record_data_name'],
                "rtype": record['data'][0]['type_name'],
                "ttl": ttl['data'][0]['ttl_name'],
                "data": content['data'][0]['content_name']
            },
            "receive": {
                "type": "block"
            }
        },
        "zone-commit": {
            "sendblock": {
                "cmd": "zone-commit",
                "zone": zone['data'][0]['zone_name']
            },
            "receive": {
                "type": "block"
            }
        }
    }
    print(json_command)
    return json_command


def zone_ns_insert(tags):
    # Get Record Data
    tags_record_data = {
        "record_data_id": tags['record_data_id']
    }
    record_data = db.row("datarecord", tags_record_data)
    tags_zone = {
        "zone_id": record_data['data'][0]['zone_id']
    }

    zone = db.row("zone", tags_zone)
    # Get Domain
    tags_domain={
        "domain_id": zone['data'][0]['domain_id']
    }
    domain = db.row("domain", tags_domain)

    # Get Record Name
    tags_type_name = {
        "type_name_id": record_data['data'][0]['type_name_id']
    }
    record = db.row("typename", tags_type_name)

    # Get ttl data
    tags_ttldata = {
        "ttl_data_id": tags['ttl_data_id']
    }
    ttldata = db.row("datattl",tags_ttldata)
    tags_ttlid = {
        "ttl_id": ttldata['data'][0]['ttl_id']
    }
    ttl = db.row("ttl",tags_ttlid)

    # Get Content
    tags_content={
        "ttl_data_id": tags['ttl_data_id']
    }
    content = db.row("content", tags_content)
    
    json_command={
        "zone-begin": {
                "sendblock": {
                "cmd": "zone-begin",
                "zone": zone['data'][0]['zone_name']
            },
            "receive": {
                "type": "block"
            }
        },
        "zone-set": {
            "sendblock": {
                "cmd": "zone-set",
                "zone": zone['data'][0]['zone_name'],
                "owner": "@",
                "rtype": record['data'][0]['type_name'],
                "ttl": ttl['data'][0]['ttl_name'],
                "data": content['data'][0]['content_name']
            },
            "receive": {
                "type": "block"
            }
        },
        "zone-commit": {
            "sendblock": {
                "cmd": "zone-commit",
                "zone": zone['data'][0]['zone_name']
            },
            "receive": {
                "type": "block"
            }
        }
    }
    print(json_command)
    return json_command




def zone_insert_srv(tags):
    tags_zone = {
        "zone_id": tags['zone_id']
    }
    zone = db.row("zone", tags_zone)
    # Get Domain
    tags_domain={
        "domain_id": zone['data'][0]['domain_id']
    }
    domain = db.row("domain", tags_domain)
    # Get Record Data
    tags_record_data = {
        "zone_id": tags['zone_id']
    }
    record_data = db.row("datarecord", tags_record_data)
    print(record_data)
    # # Get Record Name
    # tags_type_name = {
    #     "type_name_id": record_data['data'][0]['type_name_id']
    # }
    # record = db.row("typename", tags_type_name)

    # # Get ttl data
    # tags_ttldata = {
    #     "ttl_data_id": tags['ttl_data_id']
    # }
    # ttldata = db.row("datattl",tags_ttldata)
    # print(tags_ttldata)
    # tags_ttlid = {
    #     "ttl_id": ttldata['data'][0]['ttl_id']
    # }
    # ttl = db.row("ttl",tags_ttlid)

    # # Get Content
    # tags_content={
    #     "ttl_data_id": tags['ttl_data_id']
    # }
    # content = db.row("content", tags_content)
    # json_command = {
    #                     "srv-set": {
    #                         "sendblock": {
    #                             "cmd": "zone-set",
    #                             "zone": domain['data'][0]['domain_name'],
    #                             "owner": domain['data'][0]['domain_name'],
    #                             "rtype": record['data'][0]['type_name'],
    #                             "ttl": ttl['data'][0]['ttl_name'],
    #                             "data": "0 5 5060 sip.server.com."
    #                         },
    #                         "receive": {
    #                             "type": "command"
    #                         }
    #                     }
    #                 }
    # return json_command