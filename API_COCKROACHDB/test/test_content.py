import pytest
import json

content_id = ''

class TestContent:
    def test_content_get(self,client,tokentest):
        res = client.get('api/content', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_post_add(self,client,tokentest,z_datatest):
        input_add={
                    "insert": {
                        "fields": {
                            "id_ttldata": "000000000000000",
                            "nm_content": "1.1.1.1"
                        }
                            
                    }
                }

        res = client.post('api/content', 
                            data=json.dumps(input_add), 
                            content_type='application/json', 
                            headers = tokentest)

        input_add={
                    "insert": {
                        "fields": {
                            "id_ttldata": z_datatest['ttldata'][0]['id_ttldata'],
                            "nm_content": "this is test content"
                        }
                            
                    }
                }

        res = client.post('api/content', 
                            data=json.dumps(input_add), 
                            content_type='application/json', 
                            headers = tokentest)

        data = json.loads(res.data)
        global content_id
        content_id = data['message']['id']

        assert res.status_code == 200

    def test_content_post_where(self,client,tokentest,z_datatest):
        input_where={
                    "where": {
                        "tags": {
                            "id_content": z_datatest['content'][-1]['id_content']
                        }
                            
                    }
                    }
        nowhere = {
            "where" : {
                "tags" : {
                    "id_content": input_where
                }
            }
        }
        getError = client.post('api/content', 
                                data=json.dumps(nowhere), 
                                content_type='application/json', 
                                headers = tokentest)
        res = client.post('api/content', 
                            data=json.dumps(input_where), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200
        print(res.data)
        

    def test_content_remove(self,client,tokentest):
        input_rem={
                    "remove": {
                        "tags": {
                            "id_content" : content_id
                            }
                                
                        }
                    }
        inputerror = {
                    "remove": {
                        "tags": {
                            "id_content" : input_rem
                            }
                                
                        }
                    }
        reserror = client.post('api/content', 
                            data=json.dumps(inputerror), 
                            content_type='application/json', 
                            headers = tokentest)
        res = client.post('api/content', 
                            data=json.dumps(input_rem), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200

    def test_content_dataview(self, client,tokentest,z_datatest):
        input_add={
                    "view": {
                        "tags": {
                            "id_content" : z_datatest['content'][0]['id_content']
                        }
                            
                    }
                    }

        input_rem={
                    "view": {
                        "tags": {
                            "id_content" : ""
                        }
                            
                    }
                    }
        view_error = {
                    "view": {
                        "tags": {
                            "id_content" : input_rem
                        }
                            
                    }
                    }
        err = client.post('api/content', 
                            data=json.dumps(view_error), 
                            content_type='application/json', 
                            headers = tokentest)
        res_rem = client.post('api/content', 
                                data=json.dumps(input_rem), 
                                content_type='application/json', 
                                headers = tokentest)
        res = client.post('api/content', 
                            data=json.dumps(input_add), 
                            content_type='application/json', 
                            headers = tokentest)
        assert res.status_code == 200
        result = json.loads(res.data)
        print(res.data)

