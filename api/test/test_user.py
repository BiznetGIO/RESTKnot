import pytest
import json


class localData:
    ids = dict()



class TestAuth:

    var_mock = localData()

    def post_data(self,client,endpoint,data,headers):
        url = 'api/'+endpoint
        res = client.post(url,data=json.dumps(data),
                    content_type='application/json', headers=headers)
        return res

    @pytest.mark.run(order=1)
    def test_get_user_data(self,client,get_header,get_creds):
        res = client.get('api/user', headers = get_header)
        assert res.status_code == 200
        result = json.loads(res.data.decode('utf8'))
        for row in result['data']:
            if row['user_id'] == get_creds['project_id']:
                self.var_mock.ids['user_id'] = row['user_id']
                self.var_mock.ids['userdata_id'] = row['userdata_id']
                self.var_mock.ids['project_id'] = row['project_id']

    @pytest.mark.run(order=2)
    def test_insert_userdata(self,client,get_header):
        data = {"project_id" : "test", "user_id" : "test"}

        res = self.post_data(client,'user',data,get_header)
        assert res.status_code == 200

        result = json.loads(res.data.decode('utf8'))
        userdata_id = result["message"]["id"]

        self.var_mock.ids['del_id'] = userdata_id

    @pytest.mark.run(order=3)
    def test_get_userdata_by_id(self,client,get_header):
        url = 'api/user/'+self.var_mock.ids['del_id']
        res = client.get(url,headers=get_header)

        assert res.status_code

    @pytest.mark.run(order=4)
    def test_get_userdata_update(self,client,get_header):
        data = {"project_id" : "test2", "user_id" : "test2"}
        url = 'api/user/'+self.var_mock.ids['del_id']
        res = client.put(url,data=data,headers=get_header)
        assert res.status_code == 200

    @pytest.mark.run(order=5)
    def test_get_userdata_project_id(self,client,get_header,get_creds):
        url = 'api/user/project/' + get_creds['project_id']
        res = client.get(url,headers=get_header)
        assert res.status_code == 200


    @pytest.mark.run(order=6)
    def test_delete_user_data(self,client,get_header):
        url = 'api/user/'+self.var_mock.ids['del_id']
        res = client.delete(url,headers=get_header)
        assert res.status_code == 200


    def test_login(self,client,get_creds):
        """ Log In using your portal neo account """
        url = 'api/login'
        data = {"username" : get_creds['username'], "password": get_creds['password'] }
        res = client.post(url,data=json.dumps(data),content_type="application/json")
        assert res.status_code == 200



    @pytest.mark.skip
    def test_admin(self,client):
        """ Whitelist your Public IP  by adding your public ip on 'ACL' environment
        in app/middlewares/auth.py , then comment @pytest.mark.skip """
        url = 'api/zone'
        res = client.get(url)
        assert res.status_code == 200

    def test_admin_login(self,client,get_creds):
        endpoint = 'admin/login'
        data = {	"username" : get_creds['username'],
                    "password" : get_creds['password'],
                    "project_id" : get_creds['project_id']
                    }
        res = self.post_data(client,endpoint,data,None)
        assert res.status_code == 200


