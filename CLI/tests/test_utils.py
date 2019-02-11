import pytest
from libs import utils
from libs import listing as ls 
from libs import config as app
from libs import remove
from libs import auth
import requests


class TestUtils:
    @pytest.mark.run(order=0)
    def test_get_data(self):
        res = ls.get_data('ttl')
        assert res['status'] == True

    @pytest.mark.run(order=1)
    def test_get_error(self):
        res = ls.get_data(endpoint='ttl',key='id_zone')
        assert res['status'] == False

    @pytest.mark.run(order=2)
    def test_error(self, monkeypatch):
        app.setDefaultDns('test.com')
        monkeypatch.setattr("libs.config.send_request", requests.exceptions.ConnectionError)
        res = ls.list_dns()
        assert res['status'] == False

    @pytest.mark.run(order=3)
    def test_no_dns(self):
        res = ls.list_dns()
        if res['status'] :
            data = res['data']
            for row in data:
                remove.remove_zone(row)
            res = ls.list_dns()
        assert res['status'] == False

    def test_fail_parse_yaml(self):
        yaml = app.load_yaml('create_fail.yaml')
        data = app.parse_yaml(yaml['data'])
        assert data['status'] == False

    def test_load_yaml_fail(self,monkeypatch):
        yaml = app.load_yaml('create_fails.yaml')
        assert not yaml['status']

    def test_token_expired(self,monkeypatch):
        expire = {'username': 'test@biznetgio.com', 'password': 'BiznetGio2017', 'user_id': '9c2ebe8a3664b8cc847b3c61c78c30ba471d87c9110dfb25bbe9250b9aa46e91', 'project_id': 'c8b7b8ee391d40e0a8aef3b5b2860788', 'token': '528ce6a9c02e52434bbccf7d1c86b2907299e9600c6107a02aa5ce3b4a6f3592', 'timestamp': '20190201170845591819'}
        monkeypatch.setattr('libs.auth.get_env_values',lambda:expire)
        res = auth.timestamp_check()
        assert not res['status']
        monkeypatch.setattr('libs.auth.timestamp_check', lambda:res)
        auth.get_headers()

