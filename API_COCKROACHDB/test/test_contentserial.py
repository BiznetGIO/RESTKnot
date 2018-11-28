import pytest
import json

class TestContent:
    def test_content_get(self,client):
        res = client.get('api/content_serial')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_post_add(self,client):
        input_add={
                    "insert": {
                        "fields": {
                            "nm_content_serial": "38400",
                            "id_record": "402339943405944833"
                        }
                            
                    }
                    }
        res = client.post('api/content_serial', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_content_post_where(self,client):
        input_where={
                        "where": {
                            "tags": {
                                "id_content_serial" : "402146220480921601"
                            }
                                
                        }
                    }
        res = client.post('api/content_serial', data=json.dumps(input_where), content_type='application/json')
        assert res.status_code == 200

    def test_content_remove(self,client):
        input_rem={
                        "remove": {
                            "tags": {
                                "id_content_serial": "ibnu.com_soa_ctn"
                            }
                                
                        }
                    }
        res = client.post('api/content_serial', data=json.dumps(input_rem), content_type='application/json')
        assert res.status_code == 200

    def test_content_dataview(self, client):
        input_add={
                    "view": {
                        "tags": {
                            "id_content_serial" : ""
                        }
                            
                    }
                    }

        input_rem={
                    "view": {
                        "tags": {
                            "id_content" : "403085996433965057"
                        }
                            
                    }
                    }
        res_rem = client.post('api/content_serial', data=json.dumps(input_rem), content_type='application/json')
        res = client.post('api/content_serial', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200
        assert res_rem.status_code == 200