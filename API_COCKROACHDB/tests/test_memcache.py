import pytest
from app.helpers.memcache import *

class TestMemcache:
    def test_set_cache(self, client):
        data = {'email':'test@biznetgio.com'}
        result = set_cache('email', data)
        assert result

    def test_get_cache(self, client):
        data = {'email': 'test@biznetgio.com'}
        set_cache('email', data)
        result = get_cache('email')
        assert result == data

    def test_delete_cache(self, client):
        data = {'email': 'test@biznetgio.com'}
        set_cache('email', data)
        result = delete_cache('email')
        assert result