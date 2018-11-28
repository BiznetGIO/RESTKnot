import pytest
import json
from app import  db, psycopg2

class TestZone:
    def test_zone_get(self,client):
        res = client.get('api/zone')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_zone_post_add(self,client):
        json_add = {
                    "insert": {
                        "fields": {
                            "nm_zone": "ikan.com"
                            }
                            
                        }
                    }
        res = client.post('api/zone', data=json.dumps(json_add), content_type = 'application/json')
        assert res.status_code == 200

    def test_zone_post_remove(self,client):
        db.execute("SELECT id_zone FROM zn_zone WHERE nm_zone='ikan.com'")
        rows = db.fetchone()
        
        json_rem = {
                        "remove": {
                            "tags": {
                                "id_zone": rows[0]
                            }
                                
                        }
                    }
        res = client.post('api/zone', data=json.dumps(json_rem), content_type = 'application/json')
        assert res.status_code == 200

    def test_zone_post_where(self,client):
        
        #print("ROW=> ",rows[0])
        json_where = {
                        "where": {
                            "tags": {
                                "id_zone": 403088762180304897
                            }
                                
                        }
                        }
        res = client.post('api/zone', data=json.dumps(json_where), content_type='application/json')
        assert res.status_code == 200

    # def test_zone_post_double (self,client):
    #     json_rem = {
    #                     "remove": {
    #                         "tags": {
    #                             "zone_id": "iank.com"
    #                         }
                                
    #                     }
    #                 }

    #     json_add = {
    #                 "insert": {
    #                         "fields": {
    #                             "zone_name": "iank.com",
    #                             "domain_id": "iank.com"
    #                         },
    #                         "tags": {
    #                             "zone_id": "iank.com"
    #                         }
                                
    #                     }
    #                 }

    #     res_rem = client.post('api/zone', data=json.dumps(json_rem), content_type='application/json')
    #     res = client.post('api/zone', data=json.dumps(json_add), content_type='application/json')
    #     assert res.status_code == 200


