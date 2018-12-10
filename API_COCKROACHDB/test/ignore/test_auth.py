import pytest
import json
from flask import url_for, request
import hmac
import hashlib

class TestAuth:
    def test_login(self, client):
        res = client.post(
            'api/login', data={'email': 'galih@biznetgio.com', 'password': 'February2018'})
        assert res.status_code == 200
        assert res.data

    def test_account_terminated(self, client):
        res = client.post(
            'api/login', data={'email': 'rezza_ramadhan@biznetgio.com', 'password': 'BiznetGio2017'})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 401
        assert data['message'] == "Your account has been terminated"

    def test_invalid_credential(self, client):
        res = client.post(
            'api/login', data={'email': 'galih@biznetgio.com', 'password': '1234'})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 401
        assert data['message'] == "Invalid Credential"

    def test_no_account(self, client):
        res = client.post(
            'api/login', data={'email': 'aam@biznetgio.com', 'password': '1234'})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 401
        assert data['message'] == "There is no account associated with the email"
    @pytest.mark.xfail
    def test_logout(self, client,tokentest):
        algo = hashlib.sha256
        # data = bytes(request.base_url, 'UTF-8')
        # secret = bytes(request.host_url, 'UTF-8')
        data = bytes('http://localhost/api/logout', 'UTF-8')
        secret = bytes('http://localhost/', 'UTF-8')
        signature = hmac.new(secret, data, algo).hexdigest()
        # print((data, secret, signature))
        res = client.post('api/login', data={'username': 'fish', 'password':'ikan'})
        data = json.loads(res.data.decode('utf8'))
        access_token = data['data']['apikey']
        print(data)

        res = client.post('api/logout', headers={'Application-Name': 'boilerplate', 'Signature':signature, 'Access-Token':access_token})
        assert res.status_code == 200
        assert res.data
