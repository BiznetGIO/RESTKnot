import pytest
import json

class TestContent:
    def test_content_get(self,client):
        res = client.get('api/content')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_post_add(self,client):
        input_add={
                "insert": {
                    "fields": {
                        "content_name": "hostmaster.biz.net.id.",
                        "ttl_data_id": "001"
                    },
                    "tags": {
                        "content_id": "004"
                    }
                        
                }
                }
        res = client.post('api/content', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_content_post_where(self,client):
        input_where={
                    "where": {
                        "tags": {
                            "content_id": "ns1.biz.net.id."
                        }
                            
                    }
                    }
        res = client.post('api/content', data=json.dumps(input_where), content_type='application/json')
        assert res.status_code == 200

    def test_content_remove(self,client):
        input_rem={
                    "remove": {
                        "tags": {
                            "content_id": "ns1.biz.net.id."
                        }
                            
                    }
                    }
        res = client.post('api/content', data=json.dumps(input_rem), content_type='application/json')
        assert res.status_code == 200

    def test_content_post_not_double(self, client):
        input_add={
                "insert": {
                    "fields": {
                        "content_name": "hostmaster.biz.net.id.",
                        "ttl_data_id": "001"
                    },
                    "tags": {
                        "content_id": "004"
                    }
                        
                }
                }

        input_rem={
                    "remove": {
                        "tags": {
                            "content_id": "004"
                        }
                            
                    }
                    }
        res_rem = client.post('api/content', data=json.dumps(input_rem), content_type='application/json')
        res = client.post('api/content', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200
