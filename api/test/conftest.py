import requests
import json
import os
import pytest
import sys

cwd = os.getcwd()
sys.path.append(cwd)
from app import create_app,db

class MockData:
    headers = None
    data = {
        "nm_zone" : "testdns.com",
        "nm_ttl"     : "1800",
        "nm_type"   : "SOA",
        "requirements" :
        {
            "SRV" : {"nm_record": "SRVnm", "nm_type" : "SRV", "nm_ttl" : "1800", "nm_content" : "1", "nm_content_serial" : "0 50 @"},
            "MX"  : {"nm_record": "MXnm", "nm_type" : "MX", "nm_ttl" : "1800", "nm_content" : "1", "nm_content_serial" : "@"},
            "TXT" : {"nm_record": "TXTnm", "nm_type" : "TXT", "nm_ttl" : "1800", "nm_content" : "txt_content"}
    }}

    @property
    def creds(self):
        from dotenv import load_dotenv
        env_path = os.path.join(os.getcwd(),'test/.test.env')
        load_dotenv(dotenv_path=env_path) 
        creds = {
            "username" : os.getenv('CREDENTIAL_USERNAME'),
            "password"  : os.getenv('CREDENTIAL_PASSWORD'),
            "project_id": os.getenv('CREDENTIAL_PROJECT_ID'),
            "user_id": os.getenv('CREDENTIAL_USER_ID')
        }
        return creds

    @property
    def fail(self):
        from dotenv import load_dotenv
        env_path = os.path.join(os.getcwd(),'.test.env')
        load_dotenv(dotenv_path=env_path) 
        creds = {
            "username" : "TEST",
            "password"  : "TEST",
            "project_id": "TEST"
        }
        return creds

mock = MockData()
base_url = "http://127.0.0.1:6968/api/"

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture(scope='session', autouse=True)
def generate_userdata():
    try:
        res = send_userdata()
    except Exception as e:
        print(str(e))
    

@pytest.fixture(scope = 'session', autouse=True)
def request_headers():

    login_data = {"username" : mock.creds['username'],
                "password" : mock.creds['password']}
    url = base_url+'login'

    result = requests.post(url=url,data=login_data)
    result=result.json()
    token = result['data']['token']
    
    if not mock.headers:
        mock.headers = dict()
    mock.headers['Access-Token'] = token

def send_userdata():
    data = {
            "project_id": mock.creds['project_id'],
            "user_id": mock.creds['user_id']
        }
    header = {}
    login_data = {"username" : mock.creds['username'],
                "password" : mock.creds['password']}
    url = base_url+'login'

    result = requests.post(url=url,data=login_data)
    result=result.json()
    token = result['data']['token']
    headers = dict()
    headers['Access-Token'] = token
    headers['Content-Type'] = 'application/json'
    url = base_url + 'user'
    result = requests.post(url=url,data=json.dumps(data), headers=headers)
    return result

@pytest.fixture
def get_header():
    return mock.headers

@pytest.fixture
def get_mock():
    return mock.data


@pytest.fixture
def get_creds():
    return mock.creds

@pytest.fixture
def get_fail_creds():
    return mock.fail

