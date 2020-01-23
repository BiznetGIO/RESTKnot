import pytest
import pathlib
from dotenv import load_dotenv

from app import create_app
from app.models import model


@pytest.fixture(scope="module")
def clean_users():
    def _clean_users():
        # removing users will remove everything
        # since all data linked into it
        users = model.get_all("user")
        for user in users:
            user_id = user["id"]
            model.delete(table="user", field="id", value=user_id)

    return _clean_users


@pytest.fixture(scope="module")
def client():
    app = create_app()
    client = app.test_client()

    current_path = pathlib.Path(__file__)
    dotenv_path = current_path.parents[2].joinpath(".env")
    load_dotenv(dotenv_path)
    yield client

    # FIXME data can't removed using delete/truncate
    # for workaround, now using `clean_users` fixture
    # print("teardown db")
    # cursor, _ = model.get_db()
    # query = 'TRUNCATE "user" CASCADE'
    # cursor.execute(query)
