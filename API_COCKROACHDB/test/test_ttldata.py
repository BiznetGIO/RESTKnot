import pytest
import json

class TestTTLData:
    def test_ttl_data_get(self,client):
        res = client.get('api/ttldata')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_data_post_add(self,client):
        input_add = {
                        "insert": {
                            "fields": {
                                "id_record": "402475422581915649",
                                "id_ttl": "402427994557939713"
                            }
                                
                        }
                    }
        res = client.post('api/ttldata', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_ttl_data_post_where(self,client):
            input_where = {
                            "where": {
                                "tags": {
                                    "id_ttldata": "402145755976826881"
                                }
                                    
                            }
                        }
            res = client.post('api/ttldata', data=json.dumps(input_where), content_type='application/json')
            assert res.status_code == 200

    def test_ttl_data_post_rem(self,client):
            input_rem = {
                            "remove": {
                                "tags": {
                                    "id_ttldata": "402145755976826881"
                                }
                                    
                            }
                        }
            res = client.post('api/ttldata', data=json.dumps(input_rem), content_type='application/json')
            assert res.status_code == 200

    def test_ttl_data_view(self,client):
            input_rem = {
                        "view": {
                            "tags": {
                                "id_ttldata": ""
                                }
                                
                            }
                        }
            res = client.post('api/ttldata', data=json.dumps(input_rem), content_type='application/json')
            assert res.status_code == 200

    def test_ttl_data_view_2(self,client):
        view_data = {
                        "view": {
                            "tags": {
                                "id_ttldata": "403076483503357953"
                            }
                                
                        }
                    }
        res = client.post('api/record',data=json.dumps(view_data), content_type='application/json')
        assert res.status_code == 200   
