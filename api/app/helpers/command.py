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
    domain_data = db.row("domain", tags)
    domain_name = ""

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

def zone_soa_insert_default(tags):
    print(tags)
    tags_record = {
        "zone_id": tags['zone_id'],
        "record_name_id": tags['record_name_id']
    }
    
    record = db.row("datarecord", tags_record)
    tags_ttldata = {
        "ttl_data_id": tags['ttl_data_id']
    }
    ttldata = db.row("datattl",tags_ttldata)
    
    tags_ttlid = {
        "ttl_id": ttldata['data'][0]['ttl_id']
    }
    ttl = db.row("ttl",tags_ttlid)
    tags_content={
        "ttl_data_id": tags['ttl_data_id']
    }
    content = db.row("content", tags_content)

    tags_content_data ={
        "content_id": content['data'][0]['content_id']
    }
    content_data = db.row("datacontent", tags_content_data)
    return {
        "record": record,
        "ttl_data": ttldata,
        "ttl_id": ttl,
        "content": content,
        "content_data": content_data
    }

    
    # return {
    #     "record" : record
    # }
    # json_command={
    #     "zone-begin": {
    #         "sendblock": {
    #             "cmd": "zone-begin",
    #             "zone": "rosa.com"
    #         },
    #         "receive": {
    #             "type": "block"
    #         }
    #     },
    #     "soa-set": {
    #         "sendblock": {
    #             "cmd": "zone-set",
    #             "zone": "rosa.com",
    #             "owner": "rosa.com",
    #             "rtype": "SOA",
    #             "ttl": "86400",
    #             "data": "ns1.biz.net.id. hostmaster.biz.net.id. 2018070410 10800 3600 604800 38400"
    #         },
    #         "receive": {
    #             "type": "command"
    #         }
    #     },
    #     "zone-commit": {
    #         "sendblock": {
    #             "cmd": "zone-commit",
    #             "zone": "rosa.com"
    #         },
    #         "receive": {
    #             "type": "block"
    #         }
    #     }
    # }