import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.models import user as user_db


def clean_users():
    # removing users will remove everything
    # since all data linked into it
    users = user_db.get_all()
    for user in users:
        user_id = user["id"]
        user_db.delete(user_id)


@pytest.fixture
def client():
    app = FastAPI()
    _client = TestClient(app)

    yield _client

    # teardown
    clean_users()
