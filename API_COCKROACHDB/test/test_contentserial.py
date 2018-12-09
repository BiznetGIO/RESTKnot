import pytest
import json

class TestContent:
    def test_content_get(self,client,tokentest):
        res = client.get('api/content_serial', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_post_add(self,client,tokentest):
        input_add={
                    "insert": {
                        "fields": {
                            "nm_content_serial": "38400",
                            "id_record": "402339943405944833"
                        }
                            
                    }
                    }
        res = client.post('api/content_serial', 
                            data=json.dumps(input_add), 
                            content_type='application/json',
                            headers = tokentest)
        assert res.status_code == 200

    def test_content_post_where(self,client,tokentest):
        input_where={
                        "where": {
                            "tags": {
                                "id_content_serial" : "403085996399591425"
                            }
                                
                        }
                    }
        nowhere = {
            "where": {
                "tags": {
                    "id_content_serial" : input_where
                }
            }
        }
        errorRes = client.post('api/content_serial', 
                                data=json.dumps(nowhere),
                                content_type='application/json',
                                headers = tokentest
                                )
        res = client.post('api/content_serial', 
                            data=json.dumps(input_where), 
                            content_type='application/json',
                            headers = tokentest)
        result = json.loads(errorRes.data)
        assert res.status_code == 200
        assert result['message']['status'] == False

    def test_content_remove(self,client,tokentest):
        input_rem={
                        "remove": {
                            "tags": {
                                "id_content_serial": "ibnu.com_soa_ctn"
                            }
                                
                        }
                    }
        res = client.post('api/content_serial', 
                            data=json.dumps(input_rem), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200

    def test_content_dataview(self, client,tokentest):
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
                            "id_content_serial" : "403085996433965057"
                        }
                            
                    }
                    }
        res_rem = client.post('api/content_serial', 
                                data=json.dumps(input_rem), 
                                content_type='application/json', 
                                headers = tokentest)
        res = client.post('api/content_serial', 
                            data=json.dumps(input_add), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200
        assert res_rem.status_code == 200