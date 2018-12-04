import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def test_login(self,client):
    res = client.post('api/sign',data={'username': 'ikan', 'password': 'ikan'})