import pytest
import json
from app import  db, psycopg2
from test import *


def getId(self,client,namethis,tokentest):
    res = client.get('api/zone',headers = tokentest)
    data = json.loads(res.data.decode('utf8'))
    print(data)
    for result in data['data']:
        if(result['nm_zone'] == namethis):
            id_result = result['id_zone']
    return id_result

def getName(sef,client,tokentest):
    res = client.get('api/zone',headers = tokentest)
    data =json.loads(res.data.decode('utf8'))
    
    return data['data'][0]['nm_zone']

class TestZone:
    def test_zone_get(self,client,tokentest):
        res = client.get('api/zone',headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200


    def test_zone_post_add(self,client,tokentest):
        nameZone = getName(self,client,tokentest)
        json_fail = {
            "insert": {
                "fields": {
                    "nm_zone" : nameZone
                }
            }
        }
        json_add = {
                    "insert": {
                        "fields": {
                            "nm_zone": "testzone.com"
                            }
                            
                        }
                    }
        res = client.post('api/zone', 
                        data=json.dumps(json_add), 
                        content_type = 'application/json',
                        headers = tokentest
                        )
        print(res.data)
        failRes = client.post('api/zone', 
                            data=json.dumps(json_fail), 
                            content_type = 'application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200
        assert failRes.status_code == 200

    def test_zone_post_remove(self,client,tokentest):
        delete_id = getId(self,client,'testzone.com',tokentest)
        json_rem = {
                        "remove": {
                            "tags": {
                                "id_zone": delete_id
                            }
                                
                        }
                    }
        json_nowhere = {
                        "remove": {
                            "tags": {
                                "id_zone": json_rem
                            }
                                
                        }
                    }
        res = client.post('api/zone', 
                            data=json.dumps(json_rem), 
                            content_type = 'application/json',
                            headers = tokentest
                            )
        resNowhere = client.post('api/zone', 
                                data=json.dumps(json_nowhere), 
                                content_type = 'application/json',
                                headers = tokentest)
        assert res.status_code == 200
        assert resNowhere.status_code == 200

    def test_zone_post_where(self,client,tokentest,z_idtest):       
        json_where = {
                        "where": {
                            "tags": {
                                "id_zone": str(z_idtest)
                            }
                                
                        }
                        }
        json_fail = {
            "where": {
                "tags": {
                    "id_zone": json_where
                }
            }
        }
        res = client.post('api/zone', 
                            data=json.dumps(json_where), 
                            content_type='application/json',
                            headers = tokentest
                            )
        failRes = client.post('api/zone', 
                            data=json.dumps(json_fail), 
                            content_type = 'application/json',
                            headers = tokentest)
        assert res.status_code == 200
        assert failRes.status_code == 200
    
    def test_query(self,client,tokentest):
        jsonq = {
                    "query": {
                        "select": {
                            "fields": "nm_zone",
                            "where": {
                                "column" : "nm_zone",
                                "value" : "ikan.com"
                                },
                            "join": ""
                            }
                        }
                    }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = tokentest)
        assert queer.status_code == 200

    def test_query_empty(self,client,tokentest):
        jsonq = {
                    "query": {
                        "select": {
                            "fields": "nm_zone",
                            "where": "",
                            "join": ""
                            }
                        }
                    }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = tokentest)
        assert queer.status_code == 200

    def test_query_insert(self,client,tokentest):
        jsonq = {
            "query":{
                "insert": {
                    "column": {
                        "name": "nm_zone",
                    },
                    "values": {
                        "name": "monkey.com",
                    },
                    "return":  "id_zone"
                        
                    }
                }
            }
                
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = tokentest)
        assert queer.status_code == 200

    def test_query_insert_empty(self,client,tokentest):
        jsonq = {
            "query":{
                "insert": {
                    "column": {
                        "name": "",
                    },
                    "values": {
                        "name": "",
                    },
                    "return":  ""
                        
                    }
                }
            }
                
                
        queer = client.post('api/zone',
                data = json.dumps(jsonq),
                content_type = 'application/json',
                headers = tokentest)
        assert queer.status_code == 200

    