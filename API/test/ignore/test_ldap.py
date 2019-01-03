import pytest
import os
from app.libs import Ldap
from dotenv import load_dotenv, find_dotenv

class TestLdap:
    def test_account_valid(self, client):
        load_dotenv(find_dotenv())
        print(os.getenv('LDAP_HOST'))
        params = {'username':'galih@biznetgio.com', 'password':'February2018'}
        ldap = Ldap()
        connect = ldap.connect(params)
        assert connect == {}

    def test_account_invalid(self, client):
        load_dotenv(find_dotenv())
        print(os.getenv('LDAP_HOST'))
        params = {'username': 'aam@biznetgio.com',
                  'password': 'February2018'}
        ldap = Ldap()
        connect = ldap.connect(params)
        assert connect != {}
