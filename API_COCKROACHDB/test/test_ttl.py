import pytest
import json

def getId(self,client,namethis,tokentest):
    res = client.get('api/ttl',headers = tokentest)
    data = json.loads(res.data.decode('utf8'))
    for result in data['data']:
        if(result['nm_ttl'] == namethis):
            id_result = result['id_ttl']
    return id_result

def getName(sef,client,tokentest):
    res = client.get('api/ttl',headers = tokentest)
    data =json.loads(res.data.decode('utf8'))
    
    return data['data'][0]['nm_ttl']

class TestTtlName:
    def test_ttl_get(self, client,tokentest):
        res = client.get('api/ttl', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_post_add(self,client,tokentest):
        json_add = {
                    "insert": {
                        "fields": {
                            "nm_ttl": "43200"
                            }
                            
                        }
                    }

        json_new = {
            "insert": {
                "fields": {
                    "nm_ttl": "4000"
                }
            }
        }
        res = client.post('api/ttl', data=json.dumps(json_new),  content_type='application/json', headers = tokentest)
        res_d = client.post('api/ttl', data=json.dumps(json_add),  content_type='application/json', headers = tokentest)
        assert res.status_code == 200
        print('CHECK => ',res.data)


    def test_ttl_post_where(self,client,tokentest):
        json_where = {
                            "where": {
                                "tags": {
                                    "id_ttl": "402140815780249601"
                                }
                                    
                            }
                        }
        res = client.post('api/ttl', data=json.dumps(json_where),  content_type='application/json', headers = tokentest)
        assert res.status_code == 200

    def test_ttl_post_remove(self,client,tokentest):
        delete_id = getId(self,client,'4000',tokentest)

        json_rem = {
                    "remove": {
                        "tags": {
                            "id_ttl": "150"
                            }
                            
                        }
                    }
        jsondata = {
                    "remove": {
                        "tags": {
                            "id_ttl": delete_id
                            }
                            
                        }
                    }
        cleanup =  client.post('api/ttl', data=json.dumps(jsondata),  content_type='application/json', headers = tokentest)
        assert cleanup.status_code == 200
        res = client.post('api/ttl', data=json.dumps(json_rem),  content_type='application/json', headers = tokentest)
        assert res.status_code == 200

