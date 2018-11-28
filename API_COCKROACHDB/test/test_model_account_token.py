import pytest
from app.models.account import *
from app.models.account_token import *
import hashlib
from uniqid import uniqid
import arrow


class TestModelAccountToken:
    def test_insert_account_token(self, client):
        account = get_account(587)
        now = arrow.now()
        token_limit = str(now.shift(
            hours=+24).format('YYYY-MM-DD HH:mm:ss'))
        token = hashlib.md5(
            uniqid(account['owner_email']).encode('utf-8')).hexdigest()
        data = insert_account_token(account['id'], token, token_limit)
        assert data

