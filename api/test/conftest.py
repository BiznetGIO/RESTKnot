import requests
import json
import os
import pytest
import sys

sys.path.append('/home/mfriszky/worksworksworks/branch-sandbox/RESTKnot/API')
from app import create_app,db

class MockData:
    headers = None
    data = {
        "nm_zone" : "testdns.com",
        "nm_ttl"     : "1800",
        "nm_type"   : "SOA",
        "requirements" :
        {
            "SRV" : {"nm_record": "SRVnm", "nm_type" : "SRV", "nm_ttl" : "1800", "nm_content" : "srv_content", "nm_content_serial" : "serial_example"},
            "MX"  : {"nm_record": "MXnm", "nm_type" : "MX", "nm_ttl" : "1800", "nm_content" : "mx_content", "nm_content_serial" : "serial_example"},
            "TXT" : {"nm_record": "TXTnm", "nm_type" : "TXT", "nm_ttl" : "1800", "nm_content" : "txt_content"}
    }}
    creds = {"user_id" : "9c2ebe8a3664b8cc847b3c61c78c30ba471d87c9110dfb25bbe9250b9aa46e91", "project_id": "c8b7b8ee391d40e0a8aef3b5b2860788"}

    @property
    def creds(self):
        from dotenv import load_dotenv
        env_path = os.path.join(os.getcwd(),'.test.env')
        load_dotenv(env_path=env_path) 
        creds = {
            "username" : os.getenv('CREDENTIAL_USERNAME'),
            "password"  : os.getenv('CREDENTIAL_PASSWORD'),
            "project_id": os.getenv('CREDENTIAL_PROJECT_ID')
        }
        return creds

    @property
    def creds(self):
        from dotenv import load_dotenv
        env_path = os.path.join(os.getcwd(),'.test.env')
        load_dotenv(env_path=env_path) 
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

@pytest.fixture(scope = 'session', autouse=True)
def request_headers():
    
    login_data = {"username" : "test@biznetgio.com",
                "password" : "BiznetGio2017"}
    url = base_url+'login'

    result = requests.post(url=url,data=login_data)
    result=result.json()
    token = result['data']['token']
    
    if not mock.headers:
        mock.headers = dict()
    mock.headers['Access-Token'] = token

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

