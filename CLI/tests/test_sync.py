import pytest
from libs import utils
from libs import listing as ls 
from libs import config as app
from libs import remove
from libs import auth
import requests
import json
import yaml

d_data = {
            "zone": "test.com",
            "record": [
                {
                "type": "SOA",
                "name": "@",
                "content": "hostmaster",
                "ttl": "1800"
                },
                {
                "type": "NS",
                "name": "testns",
                "content": "test.com",
                "ttl": "1800"
                },
                {
                "type": "CNAME",
                "name": "testcname",
                "content": "www",
                "ttl": "1800"
                },
                {
                "type": "MX",
                "name": "testns",
                "content": "test.com",
                "ttl": "1800",
                "serial": "testserial"
                },
                {
                "type": "SRV",
                "name": "testns",
                "content": "test.com",
                "ttl": "1800",
                "serial": "1111111111"
                }
            ]
        }

list_record = list()

@pytest.fixture(autouse=True,scope= "class")
def build():
    d_data = globals()['d_data']
    d_zone = {
                "insert": {
                    "fields": {
                        "nm_zone": d_data["zone"]
                    }
                }
            }
    res = app.send_request("zone",d_zone)
    idzone = res["message"]["id"]
    global zone_id
    zone_id = idzone

    for row in d_data["record"]:
        res =create_record(row,idzone)
        to_g = {"type" : row["type"], "id_record" : res}
        globals()['list_record'].append(to_g)

    
def create_record(obj,id_zone):
    idttl = ls.get_data("ttl","id_ttl","nm_ttl",obj["ttl"])
    idttl = idttl["data"][0]
    idtype= ls.get_data("type","id_type","nm_type",obj["type"].upper())
    idtype= idtype["data"][0]

    d_record = {
                    "insert": {
                        "fields": {
                            "nm_record": obj["name"],
                            "date_record":"2018070410",
                            "id_zone": str(id_zone),
                            "id_type": str(idtype)
                        }
                    }
                }
    result = app.send_request("record",d_record)
    id_record = result["message"]["id"]

    d_ttldata = {
                "insert": {
                    "fields": {
                        "id_record": str(id_record),
                        "id_ttl": str(idttl)
                    }
                }
            }
    result = app.send_request("ttldata",d_ttldata)
    id_ttldata = result["message"]["id"]

    d_content = {
                "insert": {
                    "fields": {
                        "id_ttldata": str(id_ttldata),
                        "nm_content": obj["content"]
                    }
                }
            }
    result = app.send_request("content",d_content)

    if obj['type'] == 'SRV' or obj['type'] == 'MX':
        d_serial = {
                    "insert": {
                        "fields": {
                            "nm_content_serial": obj['serial'],
                            "id_record": id_record
                        }
                    }
                }
        app.send_request("content_serial",d_serial)

    return id_record


class TestSync():
    @pytest.mark.run(order=1)
    def test_sync_zone(self,build):
        idzone = ls.get_data("zone","id_zone","nm_zone","test.com")
        idzone = idzone['data'][0]
        d_sync = {
            "sync" : "dns",
            "data" : {
                "id_zone" : str(idzone)
            }
        }
        res = app.syncdat(d_sync)
        assert res['status']

    @pytest.mark.run(order=2)
    def test_sync_record_soa(self):
        record_data = globals()['list_record']
        check = True
        for data in record_data:
            if data["type"] == "SOA" or data["type"] == 'NS':
                sync_data = {
                    "sync" : data["type"],
                    "data" : {
                        "id_zone" : globals()['zone_id']
                    }
                }
            else :
                sync_data = {
                    "sync" : "record",
                    "data" : {
                        "type" : data["type"],
                        "id_record" : str(data["id_record"])
                    }
                }
            res=app.syncdat(sync_data)
            print(res)
            check = check and res['status']
        assert check
        del_data = {
                    "remove": {
                        "tags": {
                            "id_zone": globals()['zone_id']
                        }
                    }
                }
        app.send_request("zone",del_data)
    
