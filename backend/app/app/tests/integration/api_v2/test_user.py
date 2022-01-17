from fastapi.testclient import TestClient

from app.core.config import settings


def test_list_no_user(client: TestClient, api_key: str):
    """Test if db contains no user."""
    headers = {"X-Api-Key": api_key}
    r = client.get(f"{settings.API_V2_STR}/users/", headers=headers)
    assert r.status_code == 404


def test_crate_user(client: TestClient, api_key: str):
    """Create user from its endpoint.

    Then:
    - Check if the response appropriate
    - Query the db to assure it's created
    """
    headers = {"X-Api-Key": api_key}

    req_body = {"email": "first@company.com"}
    r_create_user = client.post(
        f"{settings.API_V2_STR}/users/", json=req_body, headers=headers
    )
    assert r_create_user.status_code == 201

    response_data = r_create_user.json()
    assert response_data["data"]["email"] == "first@company.com"

    # List user
    res = client.get(f"{settings.API_V2_STR}/users/", headers=headers)
    db_data = res.json()

    assert "first@company.com" in db_data["data"][0].values()



def test_edit_user(client: TestClient, api_key: str):
    """Edit user from its endpoint.

    Then:
    - Check if the response appropriate
    - Query the db to assure it's edited
    """
    headers = {"X-Api-Key": api_key}

    req_body = {"email": "first@company.com"}
    r_create_user = client.post(
        f"{settings.API_V2_STR}/users/", json=req_body, headers=headers
    )
    assert r_create_user.status_code == 201

    json_data = r_create_user.json()
    user_id = json_data["data"]["id"]

    req_body = {"email": "first_edited@company.com"}
    r_edit_user = client.put(
        f"{settings.API_V2_STR}/users/{user_id}", json=req_body, headers=headers
    )
    res_data = r_edit_user.json()
    assert res_data["data"]["email"] == "first_edited@company.com"

    r_get_user = client.get(f"{settings.API_V2_STR}/users/", headers=headers)
    db_data = r_get_user.json()
    assert "first_edited@company.com" in db_data["data"][0].values()


def test_delete_user(client: TestClient, api_key: str):
    """Delete user from its endpoint.

    Then:
    - Check if the response appropriate
    - Query the db to assure it's deleted
    """
    headers = {"X-Api-Key": api_key}

    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    r_delete_user = client.delete(
        f"{settings.API_V2_STR}/users/{user_id}", headers=headers
    )
    assert r_delete_user.status_code == 204

    r_list_user = client.get(f"{settings.API_V2_STR}/users", headers=headers)
    assert r_list_user.status_code == 404


def test_duplicate_email(client: TestClient, api_key: str):
    """Create multiple user with the same email.

    Must be failed.
    """
    headers = {"X-Api-Key": api_key}

    req_body = {"email": "first@company.com"}
    client.post(f"{settings.API_V2_STR}/users/", json=req_body, headers=headers)

    req_body = {"email": "first@company.com"}
    post_res = client.post(
        f"{settings.API_V2_STR}/users/", json=req_body, headers=headers
    )
    assert post_res.status_code == 409

    json_data = post_res.json()
    assert json_data["detail"] == "user with this email already exists"
