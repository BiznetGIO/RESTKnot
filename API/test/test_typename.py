import pytest
import json
from app import  db, psycopg2

name_input = "AS"
input_id = ''


class TestRecordName:
    def test_record_name_get(self, client,tokentest):
        res = client.get('api/type', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_record_name_post_add(self,client,tokentest):
        
        json_in_add = {
                        "insert": {
                            "fields": {
                                "nm_type": name_input
                            }
                        }
                    }
        res = client.post('api/type',  data=json.dumps(json_in_add),  content_type='application/json', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        global input_id
        input_id = data['message']['id']
        assert res.status_code == 200
    
    def test_record_name_post_add_fail(self,client,tokentest):
        
        json_in = {
                        "insert": {
                            "fields": {
                                "nm_type": name_input
                            }
                        }
                    }

        json_in_add = {
                        "insert": {
                            "fields": {
                                "nm_type": json_in
                            }
                        }
                    }
        res = client.post('api/type',  data=json.dumps(json_in_add),  content_type='application/json', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200
    
    def test_record_name_post_where(self,client,tokentest):
        print(input_id)
        json_in_where = {
                            "where": {
                                "tags": {
                                    "id_type": input_id
                                }
                                    
                            }
                        }
        res = client.post('api/type',
                            data=json.dumps(json_in_where),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200

    def test_record_name_post_where_fail(self,client,tokentest):
        json_in_where = {
                            "where": {
                                "tags": {
                                    "id_type": [input_id,input_id]
                                }
                                    
                            }
                        }
        res = client.post('api/type',
                            data=json.dumps(json_in_where),
                            content_type='application/json',
                            headers = tokentest
                            )

    def test_record_name_post_remove(self,client,tokentest):
        json_in_rem = {
                        "remove": {
                            "tags": {
                                "id_type": input_id
                            }
                                
                        }
                    }
        res = client.post('api/type',
                            data=json.dumps(json_in_rem),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200

    def test_record_name_post_remove_fail(self,client,tokentest):
        json_in_rem = {
                        "remove": {
                            "tags": {
                                "id_type": [input_id,input_id]
                            }
                                
                        }
                    }
        res = client.post('api/type',
                            data=json.dumps(json_in_rem),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200


