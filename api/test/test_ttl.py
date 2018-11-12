import pytest
import json

class TestTTL:
    def test_ttl_get(self, client):
        res = client.get('api/ttl')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_post_add(self,client):
        json_add = {
                        "insert": {
                                "fields": {
                                    "ttl_name": "86400"
                                },
                                "tags": {
                                    "ttl_id": "001"
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
                            "ttl_id": "001"
                        }
                            
                    }
                    }
        res = client.post('api/ttl', data=json.dumps(json_where),  content_type='application/json')
        assert res.status_code == 200

    def test_ttl_post_remove(self,client):
        json_rem = {
                "remove": {
                    "tags": {
                        "ttl_id": "001"
                    }
                        
                }
                }
        res = client.post('api/ttl', data=json.dumps(json_rem),  content_type='application/json')
        assert res.status_code == 200

    def test_ttl_post_add_double(self,client):
        json_rem = {
                "remove": {
                    "tags": {
                        "ttl_id": "001"
                    }
                        
                }
                }
        
        json_add = {
                        "insert": {
                                "fields": {
                                    "ttl_name": "86400"
                                },
                                "tags": {
                                    "ttl_id": "001"
                                }
                                
                        }
                    }
        res_rem = client.post('api/ttl', data=json.dumps(json_rem),  content_type='application/json')
        res = client.post('api/ttl', data=json.dumps(json_add),  content_type='application/json')

        assert res.status_code == 200