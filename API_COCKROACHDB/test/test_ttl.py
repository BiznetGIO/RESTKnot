import pytest
import json

class TestTtlName:
    def test_ttl_get(self, client):
        res = client.get('api/ttl')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_post_add(self,client):
        json_add = {
                    "insert": {
                        "fields": {
                            "nm_ttl": "43200"
                            }
                            
                        }
                    }
        res = client.post('api/ttl', data=json.dumps(json_add),  content_type='application/json')
        res_d = client.post('api/ttl', data=json.dumps(json_add),  content_type='application/json')
        assert res.status_code == 200


    def test_ttl_post_where(self,client):
        json_where = {
                            "where": {
                                "tags": {
                                    "id_ttl": "402140815780249601"
                                }
                                    
                            }
                        }
        res = client.post('api/ttl', data=json.dumps(json_where),  content_type='application/json')
        assert res.status_code == 200

    def test_ttl_post_remove(self,client):
        json_rem = {
                    "remove": {
                        "tags": {
                            "id_ttl": "150"
                            }
                            
                        }
                    }
        res = client.post('api/ttl', data=json.dumps(json_rem),  content_type='application/json')
        assert res.status_code == 200

    def test_ttl_post_add_double(self,client):
        json_rem = {
                    "remove": {
                        "tags": {
                            "id_ttl": "402332261606883329"
                        }
                            
                    }
                    }
        
        json_add = {
                    "insert": {
                        "fields": {
                            "nm_ttl": "43200"
                            }
                                
                        }
                    }
        res_rem = client.post('api/ttl', data=json.dumps(json_rem),  content_type='application/json')
        res = client.post('api/ttl', data=json.dumps(json_add),  content_type='application/json')

        assert res.status_code == 200