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
    def test_get_user_data(self,client,get_header):
        res = client.get('api/user', headers = get_header)
        assert res.status_code == 200
        result = json.loads(res.data.decode('utf8'))
        for row in result['data']:
            if row['user_id'] == '9c2ebe8a3664b8cc847b3c61c78c30ba471d87c9110dfb25bbe9250b9aa46e91':
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
    def test_get_userdata_project_id(self,client,get_header):
        url = 'api/user/project/' + self.var_mock.ids['project_id']
        res = client.get(url,headers=get_header)
        assert res.status_code == 200


    @pytest.mark.run(order=6)
    def test_delete_user_data(self,client,get_header):
        url = 'api/user/'+self.var_mock.ids['del_id']
        res = client.delete(url,headers=get_header)
        assert res.status_code == 200


    def test_login(self,client):
        """ Log In using your portal neo account """
        url = 'api/login'
        data = {"username" : "test@biznetgio.com", "password": "BiznetGio2017"}
        res = client.post(url,data=json.dumps(data),content_type="application/json")
        assert res.status_code == 200



    @pytest.mark.skip
    def test_admin(self,client):
        """ Whitelist your Public IP  by adding your public ip on 'ACL' environment
        in app/middlewares/auth.py , then comment @pytest.mark.skip """
        url = 'api/zone'
        res = client.get(url)
        assert res.status_code == 200





    # def test_login_expire(self, client):
    #     res = client.post(
    #         'api/sign', data={'username': 'testtoken', 'password': '1234'})
    #     result = json.loads(res.data.decode('utf8'))
    #     assert res.status_code == 200
    
    # def test_login(self,client):
    #     res = client.post(
    #         'api/sign', data={'username': 'ikan', 'password': 'fish'})
    #     result = json.loads(res.data.decode('utf8'))
    #     assert res.status_code == 200

    # def test_create_user_login(self,client,tokentest):
    #     newuser = {
    #         'username' : 'ikan',
    #         'password' : 'lauk',
    #         'userdata_id': 402435302112451777

    #     }
    #     res = client.post(
    #         'api/user/add',data=newuser
    #     )
    #     result = json.loads(res.data.decode('utf8'))
    
    # def test_get_user(self, client, tokentest):
    #     res = client.get('api/user', headers= tokentest)
    #     data = json.loads(res.data.decode('utf8'))
    #     print(data)
    #     assert data['code'] == 200

    # def test_get_user_expired(self,client,extokentest):
    #     res= client.get('api/user', headers=extokentest)
    #     data = json.loads(res.data.decode('utf8'))
    #     print(data)

    # def test_get_userbyid(self, client, tokentest):
    #     urlid = 'api/user/'
    #     id = str(402435301189451777)
    #     urlid = urlid+id
    #     res = client.get(urlid, headers= tokentest)
    #     data = json.loads(res.data.decode('utf8'))
    #     assert data['code'] == 200

    # def test_user_data_insert(self, client, tokentest):
    #     data = {
    #         'email' : 'ikanisfish@gmail.com',
    #         'first_name' : 'ikan',
    #         'last_name' : 'fish',
    #         'location' : 'laut',
    #         'city' : 'jakarta',
    #         'province' : 'dki jakarta'
    #     }

    #     data_2 = {
    #         'email' : 'kudaishorse@gmail.com',
    #         'first_name' : 'kuda',
    #         'last_name' : 'padahalhorse',
    #         'location' : 'Cisadane',
    #         'city' : 'Jakarta',
    #         'province' : 'DKI Jakarta'
    #     }

    #     res = client.post(
    #         'api/user',
    #         data=data
    #     )
    #     r = client.post(
    #         'api/user',
    #         data = data_2
    #     )
    #     result = json.loads(r.data.decode('utf8'))
    #     response = json.loads(res.data.decode('utf8'))
    #     assert response['code'] == 200
    #     assert result['code'] == 200

    # def test_user_data_update(self, client, tokentest):
    #     data = {
    #         'email' : 'ikanisfish@gmail.com',
    #         'first_name' : 'ikan',
    #         'last_name' : 'tongkol ',
    #         'location' : 'laut',
    #         'city' : 'jakarta',
    #         'province' : 'dki jakarta'
    #     }
    #     res =client.put(
    #         'api/user/397479998132813825',
    #         data=data,
    #         headers=tokentest
    #     )
    #     response = json.loads(res.data.decode('utf8'))
    #     assert response['code'] == 200

    # def test_user_data_remove(self,client,tokentest):
    #     data_id = getUserId(self,client,'kudaishorse@gmail.com',tokentest)
    #     url = 'api/user/' + str(data_id)
    #     res = client.delete(url, headers=tokentest)
    #     result = json.loads(res.data.decode('utf8'))
    #     assert result['code'] == 200

    # # def test_account_terminated(self, client):
    # #     res = client.post(
    # #         'api/login', data={'email': 'rezza_ramadhan@biznetgio.com', 'password': 'BiznetGio2017'})
    # #     data = json.loads(res.data.decode('utf8'))
    # #     assert res.status_code == 401
    # #     assert data['message'] == "Your account has been terminated"

    # # def test_invalid_credential(self, client):
    # #     res = client.post(
    # #         'api/login', data={'email': 'galih@biznetgio.com', 'password': '1234'})
    # #     data = json.loads(res.data.decode('utf8'))
    # #     assert res.status_code == 401
    # #     assert data['message'] == "Invalid Credential"
    # #@pytest.mark.xfail
    # def test_no_account(self, client):
    #     res = client.post(
    #         'api/sign', data={'username': 'ikan', 'password': '1234'})
    #     result = json.loads(res.data.decode('utf8'))
    #     assert result['code'] == 401
    
    # def test_refresh_token(self,client,refreshtokentest):
    #     pass
    #     #print(refreshtokentest)
    #     res = client.get(
    #         'api/sign/token',headers=refreshtokentest
    #     )
    #     result = json.loads(res.data.decode('utf8'))
    #     print(result)

    # # def test_logout(self, client):
    # #     algo = hashlib.sha256
    # #     # data = bytes(request.base_url, 'UTF-8')
    # #     # secret = bytes(request.host_url, 'UTF-8')
    # #     data = bytes('http://localhost/api/logout', 'UTF-8')
    # #     secret = bytes('http://localhost/', 'UTF-8')
    # #     signature = hmac.new(secret, data, algo).hexdigest()
    # #     # print((data, secret, signature))
    # #     res = client.post('api/login', data={'email': 'galih@biznetgio.com', 'password':'February2018'})
    # #     data = json.loads(res.data.decode('utf8'))
    # #     access_token = data['data']['token']


    # #     res = client.post('api/logout', headers={'Application-Name': 'boilerplate', 'Signature':signature, 'Access-Token':access_token})
    # #     assert res.status_code == 200
    # #     assert res.data
