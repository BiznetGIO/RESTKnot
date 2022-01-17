from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.models import user as user_db


def clean_users():
    # removing users will remove everything
    # since all data linked into it
    users = user_db.get_all()
    for user in users:
        user_id = user["id"]
        user_db.delete(user_id)


@pytest.fixture()
def client() -> Generator:
    with TestClient(app) as c:
        yield c

    # teardown
    clean_users()


@pytest.fixture()
def api_key() -> Dict[str, str]:
    return settings.API_KEY
