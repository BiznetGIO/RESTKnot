import pytest
import json
from app import  db, psycopg2


def getId(self,client,namethis):
    res = client.get('api/zone')
    data = json.loads(res.data.decode('utf8'))
    for result in data['data']:
        if(result['nm_zone'] == namethis):
            id_result = result['id_zone']
    return id_result

def getName(sef,client):
    res = client.get('api/zone')
    data =json.loads(res.data.decode('utf8'))
    
    return data['data'][0]['nm_zone']

class TestZone:
    def test_zone_get(self,client):
        res = client.get('api/zone')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200


    def test_zone_post_add(self,client):
        nameZone = getName(self,client)
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
                            "nm_zone": "ikan.com"
                            }
                            
                        }
                    }
        res = client.post('api/zone', data=json.dumps(json_add), content_type = 'application/json')
        failRes = client.post('api/zone', data=json.dumps(json_fail), content_type = 'application/json')
        assert res.status_code == 200
        assert failRes.status_code == 200
        print(failRes.data)

    def test_zone_post_remove(self,client):
        delete_id = getId(self,client,'ikan.com')
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
        res = client.post('api/zone', data=json.dumps(json_rem), content_type = 'application/json')
        resNowhere = client.post('api/zone', data=json.dumps(json_nowhere), content_type = 'application/json')
        assert res.status_code == 200
        assert resNowhere.status_code == 200

    def test_zone_post_where(self,client):       
        json_where = {
                        "where": {
                            "tags": {
                                "id_zone": '403088762180304897'
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
        res = client.post('api/zone', data=json.dumps(json_where), content_type='application/json')
        failRes = client.post('api/zone', data=json.dumps(json_fail), content_type = 'application/json')
        assert res.status_code == 200
        assert failRes.status_code == 200

