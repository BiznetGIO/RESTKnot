from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_domain(client: TestClient, api_key: str):
    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    res = client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    create_domain_data = res.json()
    # list domain
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_domain_data = res.json()

    assert create_domain_data["code"] == 201
    assert create_domain_data["data"]["zone"] == "company.com"
    assert list_domain_data["code"] == 200
    assert list_domain_data["data"][0]["zone"] == "company.com"
    # 4: SOA, NS, NS, CNAME
    assert len(list_domain_data["data"][0]["records"]) == 4
