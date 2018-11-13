import pytest
import json

class TestContentData:
    def test_content_data_get(self,client):
        res = client.get('api/datacontent')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_data_post_add(self,client):
        input_add={
                "insert": {
                    "fields": {
                        "content_data_name": "3600",
                        "content_data_date": "2018070410",
                        "content_id": "001"
                    },
                    "tags": {
                        "content_data_id" : "010"
                    }
                        
                }
                }
        res = client.post('api/datacontent',data=json.dumps(input_add), content_type = 'application/json')
        assert res.status_code == 200

    def test_content_data_post_where(self,client):
        input_where={
                    "where": {
                        "tags": {
                            "content_data_id" : "001"
                        }
                            
                    }
                    }
        res = client.post('api/datacontent',data=json.dumps(input_where), content_type = 'application/json')
        assert res.status_code == 200

    def test_content_data_post_rem(self,client):
        input_rem={
                "remove": {
                    "tags": {
                        "content_data_id" : "001"
                    }
                        
                }
                }
        res = client.post('api/datacontent',data=json.dumps(input_rem), content_type = 'application/json')
        assert res.status_code == 200
    
    def test_content_data_post_double_post(self, client):
        input_add={
                "insert": {
                    "fields": {
                        "content_data_name": "4500",
                        "content_data_date": "2018070410",
                        "content_id": "002"
                    },
                    "tags": {
                        "content_data_id" : "011"
                    }
                        
                }
                }
        input_rem={
                "remove": {
                    "tags": {
                        "content_data_id" : "011"
                    }
                        
                }
                }
        res_rem = client.post('api/datacontent',data=json.dumps(input_rem), content_type = 'application/json')
        res = client.post('api/datacontent',data=json.dumps(input_add), content_type = 'application/json')
        assert res.status_code == 200