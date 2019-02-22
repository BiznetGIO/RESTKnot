import pytest
import json
from app import db

ttldata_id = ''

class TestTTLData:
    def test_ttl_data_get(self,client,tokentest):
        res = client.get('api/ttldata', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_data_post_add(self,client,tokentest,z_datatest):
        input_add = {
                        "insert": {
                            "fields": {
                                "id_record": "0000000000000000",
                                "id_ttl": "000000000000000"
                            }
                                
                        }
                    }

        input_add_succ = {
                        "insert": {
                            "fields": {
                                "id_record": z_datatest['ttldata'][0]['id_record'],
                                "id_ttl": z_datatest['ttldata'][0]['id_ttl']
                            }                             
                        }
                    }

        ressuc = client.post('api/ttldata',
                            data=json.dumps(input_add_succ),
                            content_type='application/json',
                            headers = tokentest)
        res = client.post('api/ttldata',
                            data=json.dumps(input_add),
                            content_type='application/json',
                            headers = tokentest)
        data = json.loads(ressuc.data)
        global ttldata_id
        ttldata_id = data['message']['id']
        assert res.status_code == 200
        assert ressuc.status_code == 200



    def test_ttl_data_post_where(self,client,tokentest,z_datatest):
            input_where = {
                            "where": {
                                "tags": {
                                    "id_ttldata": ""
                                }
                                    
                            }
                        }
            input_where_exist = {
                "where": {
                    "tags":{
                        "id_ttldata":z_datatest['ttldata'][0]['id_ttldata']
                    }
                }
            }
            resWhere = client.post('api/ttldata',
                                    data=json.dumps(input_where_exist),
                                    content_type = 'application/json',
                                    headers = tokentest
                                    )
            res = client.post('api/ttldata', 
                                data=json.dumps(input_where), 
                                content_type='application/json',
                                headers = tokentest
                                )
            assert res.status_code == 200
            assert resWhere.status_code == 200

    def test_ttl_data_post_rem(self,client,tokentest):
            input_rem = {
                            "remove": {
                                "tags": {
                                    "id_ttldata": "000000000000000"
                                }
                                    
                            }
                        }
            
            input_rem_exist = {
                            "remove":{
                                "tags":{
                                    "id_ttldata" : ttldata_id
                                }
                            }
            }
            res = client.post('api/ttldata', 
                                data=json.dumps(input_rem), 
                                content_type='application/json',
                                headers = tokentest
                                )
            ress = client.post('api/ttldata', 
                                data=json.dumps(input_rem_exist), 
                                content_type='application/json',
                                headers = tokentest
                                )
            print(ress.data)
            assert res.status_code == 200
            assert ress.status_code == 200

    def test_ttl_data_view(self,client,tokentest):
        input_rem = {
                    "view": {
                        "tags": {
                            "id_ttldata": ""
                            }
                            
                        }
                    }
        view_data = {
                    "view": {
                        "tags": {
                            "id_ttldata": "403087860012744705"
                        }
                            
                    }
                }

        view_data_error = {
                    "view": {
                        "tags": {
                            "id_ttldata": view_data
                        }
                            
                    }
                }

        ress = client.post('api/ttldata',
                            data=json.dumps(view_data), 
                            content_type='application/json',
                            headers = tokentest
                            )
        res = client.post('api/ttldata', 
                            data=json.dumps(input_rem), 
                            content_type='application/json',
                            headers = tokentest
                            )
        resser = client.post('api/ttldata',
                            data=json.dumps(view_data_error), 
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200
        assert ress.status_code == 200
        result = json.loads(resser.data)
        assert result['data'] == None



