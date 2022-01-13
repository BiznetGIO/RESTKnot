import pathlib

import pytest
from dotenv import load_dotenv

from app import create_app
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
    current_path = pathlib.Path(__file__)
    dotenv_path = current_path.parents[2].joinpath(".env.example")
    load_dotenv(dotenv_path)

    app = create_app()
    client_ = app.test_client()

    yield client_

    # teardown
    clean_users()
