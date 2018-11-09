import pytest
import json

class TestZone:
    def test_zone_get(self,client):
        res = client.get('api/zone')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_zone_post_add(self,client):
        json_add = {
                    "insert": {
                            "fields": {
                                "zone_name": "iank.com",
                                "domain_id": "iank.com"
                            },
                            "tags": {
                                "zone_id": "iank.com"
                            }
                                
                        }
                    }
        res = client.post('api/zone', data=json.dumps(json_add), content_type = 'application/json')
        assert res.status_code == 200

    def test_zone_post_remove(self,client):
        json_rem = {
                        "remove": {
                            "tags": {
                                "zone_id": "cab.reza.com"
                            }
                                
                        }
                    }
        res = client.post('api/zone', data=json.dumps(json_rem), content_type = 'application/json')
        assert res.status_code == 200

    def test_zone_post_where(self,client):
        json_where = {
                        "where": {
                            "tags": {
                                "zone_id": "cab.reza.com"
                            }
                                
                        }
                    }
        res = client.post('api/zone', data=json.dumps(json_where), content_type='application/json')
        assert res.status_code == 200


