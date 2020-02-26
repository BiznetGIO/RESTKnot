import pathlib

import pytest
from dotenv import load_dotenv

from app import create_app
from app.models import model


def clean_users():
    # removing users will remove everything
    # since all data linked into it
    users = model.get_all("user")
    for user in users:
        user_id = user["id"]
        model.delete(table="user", field="id", value=user_id)


@pytest.fixture
def client():
    current_path = pathlib.Path(__file__)
    dotenv_path = current_path.parents[1].joinpath("test_env.env")
    load_dotenv(dotenv_path)

    app = create_app()
    client = app.test_client()

    yield client

    # teardown
    clean_users()
