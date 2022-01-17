from fastapi.testclient import TestClient

from app.core.config import settings

#
# Test CNAME Rules
#


def test_duplicate_record_CNAME(client: TestClient, api_key: str, mocker):
    """Create multiple CNAME record with same owner and rdata.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - # default CNAME owner is `www`
    - Add CNAME record with `www` as owner -> must be FAIL (duplicate record)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")

    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record
    data = {
        "zone": "company.com",
        "owner": "www",
        "rtype": "CNAME",
        "rdata": "company.com.",
        "ttl": 3600,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 409
    assert add_record_data["message"] == "record already exists"


def test_possible_duplicate_record_CNAME(client: TestClient, api_key: str, mocker):
    """Edit CNAME record that possible same with other.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - # default CNAME owner is `www`
    - Add CNAME record with `www1` as owner.
    - Edit CNAME record with `wwww` as owner and `company.com.` as rdata -> must be FAIL (duplicate record)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")

    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)

    # add record
    data = {
        "zone": "company.com",
        "owner": "www1",
        "rtype": "CNAME",
        "rdata": "company.com.",
        "ttl": 3600,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    json_data = res.json()
    record_id = json_data["data"]["id"]

    # edit possible duplicate record
    data = {
        "zone": "company.com",
        "owner": "www",
        "rtype": "CNAME",
        "rdata": "company.com.",
        "ttl": 3600,
    }
    res = client.put(
        f"{settings.API_V2_STR}/records{record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()

    assert edit_record_data["code"] == 409
    assert edit_record_data["message"] == "record already exists"


def test_unique_host(client: TestClient, api_key: str, mocker):
    """Create multiple CNAME record with different owner/host.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - # default CNAME owner is `www`
    - Add CNAME record with `www1` as owner -> must be SUCCESS (unique allowed)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")

    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record
    data = {
        "zone": "company.com",
        "owner": "www1",
        "rtype": "CNAME",
        "rdata": "company.com",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 201
    assert add_record_data["data"]["type"] == "CNAME"
    assert add_record_data["data"]["owner"] == "www1"


def test_not_unique_host(client: TestClient, api_key: str, mocker):
    """Create multiple CNAME record with same owner/host.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - # default CNAME owner is `www`
    - Add CNAME record with `www` as owner -> must be FAIL (duplicate owner)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")
    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record
    data = {
        "zone": "company.com",
        "owner": "www",
        "rtype": "CNAME",
        "rdata": "company.com",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 409
    assert add_record_data["message"] == "a CNAME record already exist with that owner"


def test_clash_with_A_owner(client: TestClient, api_key: str, mocker):
    """Create CNAME record with same A owner.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add A record with `host` as owner
    - Add CNAME record with `host` as owner -> must be FAIL (clash with A owner)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")
    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record A
    data = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    # add record
    data = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "CNAME",
        "rdata": "company.com",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 409
    assert add_record_data["message"] == "an A record already exist with that owner"


#
# Test A Rules
#


def test_duplicate_record_A(client: TestClient, api_key: str, mocker):
    """Create multiple A record with same owner and rdata.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add A record with `a1` as owner and `1.1.1.1` as rdata
    - Add A record with `a1` as owner and `1.1.1.1` as rdata -> must be FAIL (duplicate record)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")

    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record
    data = {
        "zone": "company.com",
        "owner": "a1",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)

    # add duplicate record
    data = {
        "zone": "company.com",
        "owner": "a1",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 409
    assert add_record_data["message"] == "record already exists"


def test_possible_duplicate_record_A(client: TestClient, api_key: str, mocker):
    """Edit A record that possible same with other.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add A record with `a1` as owner and `1.1.1.1` as rdata
    - Add A record with `a1` as owner and `2.2.2.2` as rdata
    - Edit A record with `a1` as owner and `1.1.1.1` as rdata -> must be FAIL (duplicate record)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")

    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record
    data = {
        "zone": "company.com",
        "owner": "a1",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)

    # add record
    data = {
        "zone": "company.com",
        "owner": "a1",
        "rtype": "A",
        "rdata": "2.2.2.2",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    json_data = res.json()
    record_id = json_data["data"]["id"]

    # edit possible duplicate record
    data = {
        "zone": "company.com",
        "owner": "a1",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    res = client.put(
        f"{settings.API_V2_STR}/records/{record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()

    assert edit_record_data["code"] == 409
    assert edit_record_data["message"] == "record already exists"


def test_not_unique_owner(client: TestClient, api_key: str, mocker):
    """Create A record with same owner.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add A record with `host` as owner
    - Add A record with `host` as owner -> must be SUCCESS (same owner allowed)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")
    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record A
    data = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    # add record A
    data = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "A",
        "rdata": "2.2.2.2",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 201
    assert add_record_data["data"]["type"] == "A"
    assert add_record_data["data"]["owner"] == "host"


def test_clash_with_cname_owner(client: TestClient, api_key: str, mocker):
    """Create A record with same CNAME owner.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add CNAME record with `host` as owner
    - Add A record with `host` as owner -> must be FAIL (clash with CNAME owner)
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")
    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)
    # add record CNAME
    data = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "CNAME",
        "rdata": "company.com",
        "ttl": 7200,
    }
    client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    # add record A
    data = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    add_record_data = res.json()

    assert add_record_data["code"] == 409
    assert add_record_data["message"] == "a CNAME record already exist with that owner"
