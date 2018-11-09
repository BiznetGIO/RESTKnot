import pytest
import json

class TestTTLData:
    def test_ttl_data_get(self,client):
        res = client.get('api/datattl')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_data_post_add(self,client):
        input_add = {
                    "insert": {
                        "fields": {
                            "ttl_data_name": "iank ttl soa record",
                            "record_data_id": "001",
                            "ttl_id": "001"
                        },
                        "tags": {
                            "ttl_data_id": "001"
                        }
                            
                    }
                    }
        res = client.post('api/datattl', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_ttl_data_post_where(self,client):
            input_where = {
                        "where": {
                            "tags": {
                                "ttl_data_id": "001"
                            }
                                
                        }
                        }
            res = client.post('api/datattl', data=json.dumps(input_where), content_type='application/json')
            assert res.status_code == 200

    def test_ttl_data_post_rem(self,client):
            input_rem = {
                        "remove": {
                            "tags": {
                                "ttl_data_id": "001"
                            }
                                
                        }
                        }
            res = client.post('api/datattl', data=json.dumps(input_rem), content_type='application/json')
            assert res.status_code == 200