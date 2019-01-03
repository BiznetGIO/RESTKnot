import pytest
import json
from flask import url_for, request
import hmac
import hashlib


class TestMiddlewareAuth:
    # def test_logout(self, client):
    #     algo = hashlib.sha256
    #     # data = bytes(request.base_url, 'UTF-8')
    #     # secret = bytes(request.host_url, 'UTF-8')
    #     data = bytes('http://localhost/api/logout', 'UTF-8')
    #     secret = bytes('http://localhost/', 'UTF-8')
    #     signature = hmac.new(secret, data, algo).hexdigest()
    #     # print((data, secret, signature))
    #     res = client.post(
    #         'api/login', data={'email': 'galih@biznetgio.com', 'password': 'February2018'})
    #     data = json.loads(res.data.decode('utf8'))
    #     access_token = data['data']['token']

    #     res = client.post('api/logout', headers={'Application-Name': 'boilerplate',
    #                                              'Signature': signature, 'Access-Token': access_token})
    #     assert res.status_code == 200
    #     assert res.data

    def test_empty_application_name(self, client):
        res = client.post('api/logout')
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 400
        assert data['message'] == 'Application-Name not Found'

    def test_invalid_application_name(self, client):
        res = client.post('api/logout', headers={'Application-Name': 'randomname'})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 404
        assert data['message'] == 'Invalid Application-Name'

    def test_empty_signature(self, client):
        res = client.post('api/logout', headers={'Application-Name': 'boilerplate'})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 400
        assert data['message'] == 'Invalid signature data'

    def test_invalid_signature(self, client):
        algo = hashlib.sha256
        signature = 'invalidsignature'
        res = client.post(
            'api/logout', headers={'Application-Name': 'boilerplate', 'Signature': signature})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 400
        assert data['message'] == 'Invalid signature data'

    def test_empty_access_token(self, client):
        algo = hashlib.sha256
        data = bytes('http://localhost/api/logout', 'UTF-8')
        secret = bytes('http://localhost/', 'UTF-8')
        signature = hmac.new(secret, data, algo).hexdigest()
        res = client.post(
            'api/logout', headers={'Application-Name': 'boilerplate', 'Signature': signature})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 400
        assert data['message'] == 'Invalid access token data'

    def test_invalid_access_token(self, client):
        algo = hashlib.sha256
        data = bytes('http://localhost/api/logout', 'UTF-8')
        secret = bytes('http://localhost/', 'UTF-8')
        signature = hmac.new(secret, data, algo).hexdigest()
        res = client.post(
            'api/logout', headers={'Application-Name': 'boilerplate', 'Signature': signature, 'Access-Token':'invalidaccesstoken'})
        data = json.loads(res.data.decode('utf8'))
        assert res.status_code == 400
        assert data['message'] == 'Wrong Token'
