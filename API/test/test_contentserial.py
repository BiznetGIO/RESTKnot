import pytest
import json

content_serial_id = ''

class TestContent:
    def test_content_get(self,client,tokentest):
        res = client.get('api/content_serial', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_post_add(self,client,tokentest,z_datatest):
        
        input_add={
                    "insert": {
                        "fields": {
                            "nm_content_serial": "38400",
                            "id_record": z_datatest['content_serial'][0]['id_record']
                        }
                            
                    }
                    }
        res = client.post('api/content_serial', 
                            data=json.dumps(input_add), 
                            content_type='application/json',
                            headers = tokentest)

        data = json.loads(res.data)
        global content_serial_id
        content_serial_id = data['message']['id']
        
        input_fail = {
                    "insert": {
                        "fields": {
                            "nm_content_serial": "38400",
                            "id_record": input_add
                        }
                            
                    }
                    }
        res_fail = client.post('api/content_serial', 
                            data=json.dumps(input_fail), 
                            content_type='application/json',
                            headers = tokentest)
        assert res.status_code == 200

    def test_content_post_where(self,client,tokentest,z_datatest):
        input_where={
                        "where": {
                            "tags": {
                                "id_content_serial" : z_datatest['content_serial'][0]['id_content_serial']
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
                                "id_content_serial": content_serial_id
                            }
                                
                        }
                    }
        res = client.post('api/content_serial', 
                            data=json.dumps(input_rem), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200

        input_rem_fail={
                        "remove": {
                            "tags": {
                                "id_content_serial": input_rem
                            }
                                
                        }
                    }
        res = client.post('api/content_serial', 
                            data=json.dumps(input_rem_fail), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200

    def test_content_dataview(self, client,tokentest,z_datatest):
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
                            "id_content_serial" : z_datatest['content_serial'][0]['id_content_serial']
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