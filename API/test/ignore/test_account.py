import pytest
import json
from flask import url_for


class TestAccount:
    def test_accounts(self, client):
        res = client.get('api/accounts')
        assert res.status_code == 200
        assert res.data

    def test_account(self, client):
        res = client.get('api/accounts')
        data = json.loads(res.data.decode('utf8'))
        account_source = data['data'][0]

        res = client.get('api/accounts/{}'.format(account_source['id']))
        data = json.loads(res.data.decode('utf8'))
        account_result = data['data']

        assert res.status_code == 200
        assert account_result == account_source

    def insertAccount(self,client):
        res = client.post(
            'api/accounts', data={'email': 'a@a.com',
                                    'first_name': 'Test',
                                    'last_name' : 'Oke',
                                    'account_state' : 'terminated'
                                    })
        assert res.status_code == 200
        assert res.data
