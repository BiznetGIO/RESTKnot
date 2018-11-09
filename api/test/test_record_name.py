import pytest
import json


class TestRecordName:
    def test_record_name_get(self, client):
        res = client.get('api/namerecord')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_record_name_post_add(self,client):
        
        json_in_add = {
                        "insert": {
                                "fields": {
                                    "record_name": "SOA"
                                },
                                "tags": {
                                    "record_name_id": "001"
                                }
                                
                        }
                    }
        res = client.post('api/namerecord',  data=json.dumps(json_in_add),  content_type='application/json')
        assert res.status_code == 200
    
    def test_record_name_post_where(self,client):
        json_in_where = {
                        "where": {
                                "tags": {
                                    "record_name_id": "001"
                                }
                                    
                            }
                        }
        res = client.post('api/namerecord',  data=json.dumps(json_in_where),  content_type='application/json')
        assert res.status_code == 200

    def test_record_name_post_remove(self,client):
        json_in_rem = {
                        "remove": {
                            "tags": {
                                "record_name_id": "001"
                            }
                                
                        }
                    }
        res = client.post('api/namerecord',  data=json.dumps(json_in_rem),  content_type='application/json')
        assert res.status_code == 200


