import pytest
import json

class TestDomain:
    def test_domain_get(self, client):
        res = client.get('api/domain')
        data = json.loads(res.data.decode('utf8'))
            
        assert res.status_code == 200
    
    def test_domain_post_add(self, client):
        json_d_add = {
                    "insert": {
                        "fields": {
                            "domain_name": "iank.com"
                        },
                        "tags": {
                            "domain_id": "iank.com"
                        }
                            
                    }
                }
        res = client.post('api/domain', data=json.dumps(json_d_add),  content_type='application/json')
        assert res.status_code == 200
    
    def test_domain_post_where(self, client):
        json_d_whe = {
                    "where": {
                                "tags": {
                                    "domain_id": "reza.com"
                                }	
                            }
                }
        res = client.post('api/domain', data=json.dumps(json_d_whe),  content_type='application/json')
        assert res.status_code == 200


    def test_domain_post_remove(self, client):
        json_d_rem = {
                        "remove": {
                                "tags": {
                                    "domain_id": "reza2.com"
                                }	
                        }
                    }
        res = client.post('api/domain', data=json.dumps(json_d_rem),  content_type='application/json')
        
        assert res.status_code == 200
        
    def test_domain_post_add_nondouble(self, client):
        json_d_rem = {
                        "remove": {
                                "tags": {
                                    "domain_id": "iank.com"
                                }	
                        }
                    }
        res_rem = client.post('api/domain', data=json.dumps(json_d_rem),  content_type='application/json')

        json_d_add = {
                    "insert": {
                        "fields": {
                            "domain_name": "iank.com"
                        },
                        "tags": {
                            "domain_id": "iank.com"
                        }
                            
                    }
                }
        res = client.post('api/domain', data=json.dumps(json_d_add),  content_type='application/json')
        assert res.status_code == 200


