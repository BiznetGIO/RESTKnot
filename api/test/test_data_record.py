import pytest
import json

class TestDataRecord:
    def test_data_record_get(self,client):
        res = client.get('api/datarecord')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_data_record_post_add(self,client):
        
        input_add={
                "insert": {
                        "fields": {
                            "record_data_name": "iank soa record",
                            "record_name_id": "001",
                            "zone_id": "iank.com"
                        },
                        "tags": {
                            "record_data_id": "002"
                        }
                            
                    }
                }
        res = client.post('api/datarecord',data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_data_record_post_where(self,client):
        
        input_where={
                        "where": {
                            "tags": {
                                "record_data_id": "001"
                            }
                                
                        }
                    }
        res = client.post('api/datarecord',data=json.dumps(input_where), content_type='application/json')
        assert res.status_code == 200

    def test_data_record_post_remove(self,client):
        
        input_rem={
                "remove": {
                        "tags": {
                            "record_data_id": "001"
                        }
                            
                    }
                }
        res = client.post('api/datarecord',data=json.dumps(input_rem), content_type='application/json')
        assert res.status_code == 200