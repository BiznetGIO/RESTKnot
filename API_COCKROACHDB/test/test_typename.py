import pytest
import json
from app import  db, psycopg2

name_input = "AS"

def getId(self,client,namethis,tokentest):
    res = client.get('api/type',headers = tokentest)
    data = json.loads(res.data.decode('utf8'))
    print(data)
    for result in data['data']:
        if(result['nm_type'] == namethis):
            id_result = result['id_type']
    return id_result

def getData(sef,client,tokentest):
    retdat = dict()
    res = client.get('api/type',headers = tokentest)
    data =json.loads(res.data.decode('utf8'))
    retdat['id_type'] = data['data'][0]['id_type']
    retdat['nm_type'] = data['data'][0]['nm_type']
    return retdat

class TestRecordName:
    def test_record_name_get(self, client,tokentest):
        res = client.get('api/type', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_record_name_post_add(self,client,tokentest):
        
        json_in_add = {
                        "insert": {
                            "fields": {
                                "nm_type": name_input
                            }
                        }
                    }
        res = client.post('api/type',  data=json.dumps(json_in_add),  content_type='application/json', headers = tokentest)
        assert res.status_code == 200
    
    def test_record_name_post_where(self,client,tokentest):
        obj = getData(self,client,tokentest)
        json_in_where = {
                            "where": {
                                "tags": {
                                    "id_type": obj['id_type']
                                }
                                    
                            }
                        }
        res = client.post('api/type',
                            data=json.dumps(json_in_where),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200

    def test_record_name_post_remove(self,client,tokentest):
        id_delete = getId(self,client,name_input,tokentest)
        json_in_rem = {
                        "remove": {
                            "tags": {
                                "id_type": id_delete[0]
                            }
                                
                        }
                    }
        res = client.post('api/type',
                            data=json.dumps(json_in_rem),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200


