import pytest
import json

class TestContent:
    def test_content_get(self,client):
        res = client.get('api/content')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_content_post_add(self,client):
        input_add={
                    "insert": {
                        "fields": {
                            "id_ttldata": "403085996278251521",
                            "nm_content": "1.1.1.1"
                        }
                            
                    }
                }

        res = client.post('api/content', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200

    def test_content_post_where(self,client):
        input_where={
                    "where": {
                        "tags": {
                            "id_content": "403086715543289857"
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
        getError = client.post('api/content', data=json.dumps(nowhere), content_type='application/json')
        res = client.post('api/content', data=json.dumps(input_where), content_type='application/json')
        assert res.status_code == 200
        print(res.data)
        

    def test_content_remove(self,client):
        input_rem={
                    "remove": {
                        "tags": {
                            "id_content" : "403076483136723169"
                            }
                                
                        }
                    }
        print("DS")
        res = client.post('api/content', data=json.dumps(input_rem), content_type='application/json')
        assert res.status_code == 200

    def test_content_dataview(self, client):
        input_add={
                    "view": {
                        "tags": {
                            "id_content" : "403531114509959169"
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
        res_rem = client.post('api/content', data=json.dumps(input_rem), content_type='application/json')
        res = client.post('api/content', data=json.dumps(input_add), content_type='application/json')
        assert res.status_code == 200
        result = json.loads(res.data)
        print(res.data)

