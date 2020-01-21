import pytest
from dotenv import load_dotenv

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    load_dotenv()
    return client
