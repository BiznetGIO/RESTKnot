import pytest
from app import create_app
import requests
import json

headers = dict()
expirehead = dict()

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture(scope = 'session', autouse=True)
def tokenTest():
    response=requests.request("POST",url='http://127.0.0.1:6968/api/sign', data={'username': 'ikan', 'password': 'fish'})
    result = response.json()
    tokensession=result['data']['apikey']
    global headers
    headers = {
            'Authorization' : str(tokensession)
        }
    print("ONLY ONCE")
    return headers

@pytest.fixture(scope = 'module', autouse=True)
def expiredToken():
    response=requests.request("POST",url='http://127.0.0.1:6968/api/sign', data={'username': 'testtoken', 'password': '1234'})
    result = response.json()
    extokensession=result['data']['apikey']
    global expirehead
    expirehead = {
            'Authorization' : str(extokensession)
        }
    print("ONLY ONCE")
    return expirehead

@pytest.fixture
def extokentest():
    return expirehead

@pytest.fixture(autouse=True)
def tokentest():
    return headers
