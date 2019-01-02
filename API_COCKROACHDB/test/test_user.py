import pytest
import json
from flask import url_for, request
import hmac
import hashlib
import time
from app.middlewares.auth import * 


def getUserId(self,client,email,tokentest):
    res = client.get('api/user', headers=tokentest)
    data = json.loads(res.data.decode('utf8'))
    data = data['data']
    for row in data:
        if row['email'] == email:
            id_result = row['userdata_id']
    return id_result

class TestAuth:
    def test_login_expire(self, client):
        res = client.post(
            'api/sign', data={'username': 'testtoken', 'password': '1234'})
        result = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200
    
    def test_login(self,client):
        res = client.post(
            'api/sign', data={'username': 'ikan', 'password': 'fish'})
        result = json.loads(res.data.decode('utf8'))
        assert res.status_code == 200

    def test_create_user_login(self,client,tokentest):
        newuser = {
            'username' : 'ikan',
            'password' : 'lauk',
            'userdata_id': 402435302112451777

        }
        res = client.post(
            'api/user/add',data=newuser
        )
        result = json.loads(res.data.decode('utf8'))
    
    def test_get_user(self, client, tokentest):
        res = client.get('api/user', headers= tokentest)
        data = json.loads(res.data.decode('utf8'))
        print(data)
        assert data['code'] == 200

    def test_get_user_expired(self,client,extokentest):
        res= client.get('api/user', headers=extokentest)
        data = json.loads(res.data.decode('utf8'))
        print(data)

    def test_get_userbyid(self, client, tokentest):
        urlid = 'api/user/'
        id = str(402435301189451777)
        urlid = urlid+id
        res = client.get(urlid, headers= tokentest)
        data = json.loads(res.data.decode('utf8'))
        assert data['code'] == 200

    def test_user_data_insert(self, client, tokentest):
        data = {
            'email' : 'ikanisfish@gmail.com',
            'first_name' : 'ikan',
            'last_name' : 'fish',
            'location' : 'laut',
            'city' : 'jakarta',
            'province' : 'dki jakarta'
        }

        data_2 = {
            'email' : 'kudaishorse@gmail.com',
            'first_name' : 'kuda',
            'last_name' : 'padahalhorse',
            'location' : 'Cisadane',
            'city' : 'Jakarta',
            'province' : 'DKI Jakarta'
        }

        res = client.post(
            'api/user',
            data=data
        )
        r = client.post(
            'api/user',
            data = data_2
        )
        result = json.loads(r.data.decode('utf8'))
        response = json.loads(res.data.decode('utf8'))
        assert response['code'] == 200
        assert result['code'] == 200

    def test_user_data_update(self, client, tokentest):
        data = {
            'email' : 'ikanisfish@gmail.com',
            'first_name' : 'ikan',
            'last_name' : 'tongkol ',
            'location' : 'laut',
            'city' : 'jakarta',
            'province' : 'dki jakarta'
        }
        res =client.put(
            'api/user/397479998132813825',
            data=data,
            headers=tokentest
        )
        response = json.loads(res.data.decode('utf8'))
        assert response['code'] == 200

    def test_user_data_remove(self,client,tokentest):
        data_id = getUserId(self,client,'kudaishorse@gmail.com',tokentest)
        url = 'api/user/' + str(data_id)
        res = client.delete(url, headers=tokentest)
        result = json.loads(res.data.decode('utf8'))
        assert result['code'] == 200

    # def test_account_terminated(self, client):
    #     res = client.post(
    #         'api/login', data={'email': 'rezza_ramadhan@biznetgio.com', 'password': 'BiznetGio2017'})
    #     data = json.loads(res.data.decode('utf8'))
    #     assert res.status_code == 401
    #     assert data['message'] == "Your account has been terminated"

    # def test_invalid_credential(self, client):
    #     res = client.post(
    #         'api/login', data={'email': 'galih@biznetgio.com', 'password': '1234'})
    #     data = json.loads(res.data.decode('utf8'))
    #     assert res.status_code == 401
    #     assert data['message'] == "Invalid Credential"
    #@pytest.mark.xfail
    def test_no_account(self, client):
        res = client.post(
            'api/sign', data={'username': 'ikan', 'password': '1234'})
        result = json.loads(res.data.decode('utf8'))
        assert result['code'] == 401
    
    def test_refresh_token(self,client,refreshtokentest):
        pass
        #print(refreshtokentest)
        res = client.get(
            'api/sign/token',headers=refreshtokentest
        )
        result = json.loads(res.data.decode('utf8'))
        print(result)

    # def test_logout(self, client):
    #     algo = hashlib.sha256
    #     # data = bytes(request.base_url, 'UTF-8')
    #     # secret = bytes(request.host_url, 'UTF-8')
    #     data = bytes('http://localhost/api/logout', 'UTF-8')
    #     secret = bytes('http://localhost/', 'UTF-8')
    #     signature = hmac.new(secret, data, algo).hexdigest()
    #     # print((data, secret, signature))
    #     res = client.post('api/login', data={'email': 'galih@biznetgio.com', 'password':'February2018'})
    #     data = json.loads(res.data.decode('utf8'))
    #     access_token = data['data']['token']


    #     res = client.post('api/logout', headers={'Application-Name': 'boilerplate', 'Signature':signature, 'Access-Token':access_token})
    #     assert res.status_code == 200
    #     assert res.data
