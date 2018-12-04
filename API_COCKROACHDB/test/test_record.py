import pytest
import json
from app import db

class TestDataRecord:
    
    def test_data_record_get(self,client):
        res = client.get('api/record')
        data = json.loads(res.data.decode('utf8'))
        ress = client.get('api/records')
        assert ress.status_code == 404
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

        input_add_success={
                    "insert": {
                        "fields": {
                            "nm_record":"tekukur",
                            "date_record":"2018070410",
                            "id_zone":"403087859506577409",
                            "id_type":"402386688803307521"
                        }
                            
                    }            
                }

        res = client.post('api/record',data=json.dumps(input_add), content_type='application/json')
        resSuc = client.post('api/record',data=json.dumps(input_add_success), content_type='application/json')
        assert res.status_code == 200
        assert resSuc.status_code == 200

    def test_data_record_post_where(self,client):
        
        input_where={
                        "where": {
                            "tags": {
                                "id_record": "403086715296612353"
                                
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
        resError = client.post('api/record',data=json.dumps(nowhere), content_type='application/json')
        res = client.post('api/record',data=json.dumps(input_where), content_type='application/json')
        result = json.loads(resError.data)
        print(resError.data)
        print("STAT = ",result['message']['status'])
        assert res.status_code == 200

    def test_data_record_post_remove(self,client):
        query = """SELECT id_record FROM zn_record WHERE nm_record='tekukur' AND id_zone='403087859506577409'
        AND id_type='402386688803307521' AND date_record='2018070410'
        """
        db.execute(query)
        rows=db.fetchone()
        print(rows)

        cleanup = {
                    "remove":{
                        "tags":{
                            "id_record": str(rows[0])
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
        resclean = client.post('api/record',data=json.dumps(cleanup),content_type='application/json')
        res = client.post('api/record',data=json.dumps(input_rem), content_type='application/json')
        assert resclean.status_code == 200
        assert res.status_code == 200

    def test_daata_record_view(self,client):
        view_data = {
                    "view": {
                        "tags": {
                            "id_record": "403531114140762113"
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

        resNone = client.post('api/record',data=json.dumps(view_data_none), content_type='application/json')
        resErr = client.post('api/record',data=json.dumps(view_datas), content_type='application/json')
        res = client.post('api/record',data=json.dumps(view_data), content_type='application/json')
        assert res.status_code == 200
        assert resErr.status_code == 200
        assert resNone.status_code == 200

 

    