import pytest
import json
from app import db

class TestTTLData:
    def test_ttl_data_get(self,client):
        res = client.get('api/ttldata')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_ttl_data_post_add(self,client):
        input_add = {
                        "insert": {
                            "fields": {
                                "id_record": "402475422581915649",
                                "id_ttl": "402427994557939713"
                            }
                                
                        }
                    }

        input_add_succ = {
                        "insert": {
                            "fields": {
                                "id_record": "403076483056435201",
                                "id_ttl": "402427936007192577"
                            }
                                
                        }
                    }

        ressuc = client.post('api/ttldata', data=json.dumps(input_add_succ), content_type='application/json')
        res = client.post('api/ttldata', data=json.dumps(input_add), content_type='application/json')
        
        assert res.status_code == 200
        assert ressuc.status_code == 200

    def test_ttl_data_post_where(self,client):
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
                        "id_ttldata":"403076483503357953"
                    }
                }
            }
            resWhere = client.post('api/ttldata', data=json.dumps(input_where_exist), content_type = 'application/json')
            res = client.post('api/ttldata', data=json.dumps(input_where), content_type='application/json')
            assert res.status_code == 200
            assert resWhere.status_code == 200

    def test_ttl_data_post_rem(self,client):
            db.execute("SELECT id_ttldata FROM zn_ttldata WHERE id_record = 403076483056435201 AND id_ttl = 402427936007192577")
            rows = db.fetchone()
            print(rows[0])
            input_rem = {
                            "remove": {
                                "tags": {
                                    "id_ttldata": "402145755976826881"
                                }
                                    
                            }
                        }

            input_rem_exist = {
                            "remove":{
                                "tags":{
                                    "id_ttldata" : rows[0]
                                }
                            }
            }
            res = client.post('api/ttldata', data=json.dumps(input_rem), content_type='application/json')
            ress = client.post('api/ttldata', data=json.dumps(input_rem), content_type='application/json')
            assert res.status_code == 200
            assert ress.status_code == 200

    def test_ttl_data_view(self,client):
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
                            "id_ttldata": "403463031350493185"
                        }
                            
                    }
                }
        ress = client.post('api/ttldata',data=json.dumps(view_data), content_type='application/json')
        res = client.post('api/ttldata', data=json.dumps(input_rem), content_type='application/json')
        assert res.status_code == 200
        assert ress.status_code == 200

    def test_view(self,client):
        ququ = "SELECT * FROM v_ttldata WHERE id_ttldata = 403463031350493185"
        db.execute(ququ);
        rows=db.fetchall()
        print("RRR = ", rows)