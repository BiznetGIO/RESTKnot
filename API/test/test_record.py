import pytest
import json

record_id = ''

class TestDataRecord:
    def test_data_record_get(self,client,tokentest):
        res = client.get('api/record', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_data_record_post_add(self,client,tokentest,z_datatest):        
        data_id = z_datatest
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

        input_add_success={
                    "insert": {
                        "fields": {
                            "nm_record":"tekukur",
                            "date_record": z_datatest['record'][0]['date_record'],
                            "id_zone": z_datatest['record'][0]['id_zone'],
                            "id_type": z_datatest['record'][0]['id_type']
                        }
                            
                    }            
                }

        res = client.post('api/record',data=json.dumps(input_add), content_type='application/json', headers=tokentest)
        resSuc = client.post('api/record',data=json.dumps(input_add_success), content_type='application/json', headers=tokentest)
        data = json.loads(resSuc.data)
        global record_id
        record_id = data['message']['id']
        print("LOCAL ", record_id)
        assert res.status_code == 200
        assert resSuc.status_code == 200

    def test_data_record_post_where(self,client,tokentest,z_datatest):
        
        input_where={
                        "where": {
                            "tags": {
                                "id_record": z_datatest['record'][0]['id_record']
                                
                            }
                                
                        }
                        }
        nowhere={
                        "where": {
                            "tags": {
                                "id_record": input_where
                                
                            }
                                
                        }
                        }
        resError = client.post('api/record',data=json.dumps(nowhere), content_type='application/json', headers=tokentest)
        res = client.post('api/record',data=json.dumps(input_where), content_type='application/json', headers=tokentest)
        result = json.loads(resError.data)
        assert res.status_code == 200

    def test_data_record_post_remove(self,client,tokentest):

        cleanup = {
                    "remove":{
                        "tags":{
                            "id_record": record_id
                        }
                    }
        }

        input_rem={
                    "remove": {
                        "tags": {
                            "id_record": "448f77074b4c5ed5b08c56384b276900"
                        }
                            
                    }
                    }
        resclean = client.post('api/record',data=json.dumps(cleanup),content_type='application/json', headers=tokentest)
        res = client.post('api/record',data=json.dumps(input_rem), content_type='application/json', headers=tokentest)
        assert resclean.status_code == 200
        assert res.status_code == 200

    def test_daata_record_view(self,client,tokentest,z_datatest):
        view_data = {
                    "view": {
                        "tags": {
                            "id_record": z_datatest['record'][0]['id_record']
                        }
                    }
                    }
        
        view_datas = {
                        "view": {
                            "tags": {
                                "id_record": view_data
                            }
                                
                        }
                    }
        
        view_data_none = {
                        "view": {
                            "tags": {
                                "id_record": ""
                            }
                                
                        }
                    }

        resNone = client.post('api/record',data=json.dumps(view_data_none), content_type='application/json', headers=tokentest)
        resErr = client.post('api/record',data=json.dumps(view_datas), content_type='application/json', headers=tokentest)
        res = client.post('api/record',data=json.dumps(view_data), content_type='application/json', headers=tokentest)
        assert res.status_code == 200
        assert resErr.status_code == 200
        assert resNone.status_code == 200

 

    