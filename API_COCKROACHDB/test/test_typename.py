import pytest
import json
from app import  db, psycopg2

class TestRecordName:
    def test_record_name_get(self, client,tokentest):
        res = client.get('api/type', headers = tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_record_name_post_add(self,client,tokentest):
        
        json_in_add = {
                        "insert": {
                            "fields": {
                                "nm_type": "AS"
                            }
                        }
                    }
        res = client.post('api/type',  data=json.dumps(json_in_add),  content_type='application/json', headers = tokentest)
        assert res.status_code == 200
    
    def test_record_name_post_where(self,client,tokentest):
        json_in_where = {
                            "where": {
                                "tags": {
                                    "id_type": "402140280385142785"
                                }
                                    
                            }
                        }
        res = client.post('api/type',
                            data=json.dumps(json_in_where),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200

    def test_record_name_post_remove(self,client,tokentest):
        db.execute("SELECT id_type FROM zn_type WHERE nm_type='AS'")
        rows = db.fetchone()
        print(rows[0])
        json_in_rem = {
                        "remove": {
                            "tags": {
                                "id_type": rows[0]
                            }
                                
                        }
                    }
        res = client.post('api/type',
                            data=json.dumps(json_in_rem),
                            content_type='application/json',
                            headers = tokentest
                            )
        assert res.status_code == 200


