import pytest
import json


class TestUser:
    def test_get_user(self,client):
        res = client.get('api/user')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    # def test_user_post_add(self,client):
    #     send_data = {
    #                 "insert": {
    #                     "fields": {
    #                         "email": "test",
    #                         "first_name": "test",
    #                         "last_name": "test",
    #                         "city": "test",
    #                         "province": "test",
    #                         "location": "test",
    #                         "created_at" : "now"
    #                         }
    #                     }
    #                 }
    #     res = client.post('api/user', data=json.dumps(send_data), content_type='application/json')
    #     assert res.status_code == 200
