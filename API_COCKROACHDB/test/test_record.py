import pytest
import json

class TestDataRecord:
    def test_data_record_get(self,client):
        res = client.get('api/record')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_data_record_post_add(self,client):
        
        input_add={
                    "insert": {
                        "fields": {
                            "nm_record":"tekukur",
                            "date_record":"2018070410",
                            "id_zone":"402468020781678593",
                            "id_type":"402427545745850369"
                        }
                            
                    }
                }
        res = client.post('api/record',data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_data_record_post_where(self,client):
        
        input_where={
                        "where": {
                            "tags": {
                                "id_record": "402145661681991681"
                                
                            }
                                
                        }
                        }
        res = client.post('api/record',data=json.dumps(input_where), content_type='application/json')
        assert res.status_code == 200

    def test_data_record_post_remove(self,client):
        
        input_rem={
                    "remove": {
                        "tags": {
                            "id_record": "448f77074b4c5ed5b08c56384b276900"
                        }
                            
                    }
                    }
        res = client.post('api/record',data=json.dumps(input_rem), content_type='application/json')
        assert res.status_code == 200

    def test_daata_record_view(self,client):
        view_data = {
                        "view": {
                            "tags": {
                                "id_record": ""
                            }
                                
                        }
                    }
        res = client.post('api/record',data=json.dumps(view_data), content_type='application/json')
        assert res.status_code == 200

    def test_daata_record_view_2(self,client):
        view_data = {
                        "view": {
                            "tags": {
                                "id_record": "403531114140762113"
                            }
                                
                        }
                    }
        res = client.post('api/record',data=json.dumps(view_data), content_type='application/json')
        assert res.status_code == 200   
