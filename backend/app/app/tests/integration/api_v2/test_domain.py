from fastapi.testclient import TestClient

import app.helpers.producer
from app.core.config import settings


def test_list_no_domain(client: TestClient, api_key: str):
    """Test if db contains no domain."""
    headers = {"X-Api-Key": api_key}
    r_get_domains = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    assert r_get_domains.status_code == 404


def test_domain(client: TestClient, api_key: str, mocker):
    """Test domain happy path.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - List the domain
    - Delete the domain
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")
    headers = {"X-Api-Key": api_key}

    # create user
    req_body = {"email": "first@company.com"}
    post_res = client.post(
        f"{settings.API_V2_STR}/users/", json=req_body, headers=headers
    )
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # Add domain
    req_body = {"zone": "company.com", "user_id": user_id}
    r_create_domain = client.post(
        f"{settings.API_V2_STR}/domains/", json=req_body, headers=headers
    )
    import ipdb; ipdb.set_trace()
    assert r_create_domain.status_code == 201

    create_domain_data = r_create_domain.json()
    assert create_domain_data["data"]["zone"] == "company.com"

    # List domain
    r_get_domains = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    assert r_get_domains.status_code == 200

    get_domains_data = r_get_domains.json()
    assert get_domains_data["data"][0]["zone"] == "company.com"
    # 4: SOA, NS, NS, CNAME
    assert len(get_domains_data["data"][0]["records"]) == 4
    # TODO can we assert the result of `call_args` since using `call_with`
    # is not feasible way knowing the very long arguments

    # Delete domain
    zone_to_delete = "company.com"
    r_delete_domain = client.delete(f"{settings.API_V2_STR}/domains/zone/{zone_to_delete}", headers=headers)
    import ipdb; ipdb.set_trace()
    assert r_delete_domain.status_code == 204


    # 4: set_config, set_zone, delegate, delegate (creation)
    # 5: unset_config, unset_zone (SOA, NS, NS, CNAME)

    # Call count: 9 if using `set_default_zone`, 12 if using `set_zone`
    assert app.helpers.producer.send.call_count == 12  # pylint: disable=no-member
