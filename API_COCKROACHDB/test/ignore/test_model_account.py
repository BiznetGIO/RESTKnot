import pytest
from app.models.account import *

class TestModelAccount:
    def test_get_accounts(self, client):
        data = Account.objects.all()
        assert data
