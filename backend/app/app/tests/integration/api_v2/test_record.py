import datetime

from fastapi.testclient import TestClient

from app.api.api_v2.endpoints import record as record_api
from app.core.config import settings
from app.helpers import helpers
from app.models import rtype as rtype_db
from app.models import ttl as ttl_db


def get_record(records, target_type):
    type_ = rtype_db.get_by_value(target_type)

    for record in records:
        if record["rtype_id"] == type_["id"]:
            return record


def test_list_no_record(client: TestClient, api_key: str):
    """Test if db contains no record."""
    headers = {"X-Api-Key": api_key}
    r_read_domains = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    r_read_domains.status_code = 404


def test_add_record(client: TestClient, api_key: str, mocker):
    """Test adding record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add a record
    - Query the db to assure it's created
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    mocker.patch("app.helpers.producer.send")
    headers = {"X-Api-Key": api_key}

    # create user
    req_body = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=req_body, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    req_body = {"zone": "company.com", "user_id": user_id}
    r_add_domain = client.post(f"{settings.API_V2_STR}/domains/", json=req_body, headers=headers)
    assert r_add_domain.status_code == 201

    add_domain_data = r_add_domain.json()
    assert add_domain_data["data"]["zone"] == "company.com"

    # add record
    req_body = {
        "zone": "company.com",
        "owner": "host",
        "rtype": "A",
        "rdata": "1.1.1.1",
        "ttl": 7200,
    }
    r_add_record = client.post(f"{settings.API_V2_STR}/records/", json=req_body, headers=headers)
    import ipdb; ipdb.set_trace()
    assert r_add_record.status_code == 201

    add_record_data = r_add_record.json()
    assert add_record_data["data"]["owner"] == "host"
    assert add_record_data["data"]["rdata"] == "1.1.1.1"

    # list record
    r_read_domains = client.get(f"{settings.API_V2_STR}/domains/", headers=headers)
    assert r_read_domains.status_code == 200

    list_record_data = r_read_domains.json()
    assert list_record_data["data"][0]["zone"] == "company.com"
    assert list_record_data["data"][0]["user"]["email"] == "first@company.com"


def test_edit_record(client: TestClient, api_key: str, mocker):
    """Test editing record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add a record
    - Edit a record
    - Query the db to assure it's edited
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
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    # edit record
    records = list_record_data["data"][0]["records"]
    cname_record = get_record(records, "CNAME")
    cname_record_id = cname_record["id"]
    data = {
        "zone": "company.com",
        "owner": "www_edit",
        "rtype": "CNAME",
        "rdata": "company_edited.com",
        "ttl": 3600,
    }
    res = client.put(
        f"{settings.API_V2_STR}/records{cname_record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    records = list_record_data["data"][0]["records"]
    edited_record_data = get_record(records, "CNAME")

    assert edit_record_data["code"] == 200
    assert edit_record_data["data"]["owner"] == "www_edit"

    assert list_record_data["code"] == 200
    assert edited_record_data["rdata"] == "company_edited.com"


def test_edit_record_no_ttl_change(client: TestClient, api_key: str, mocker):
    """Test editing record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Edit a record with the same TTL
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
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    # edit record
    records = list_record_data["data"][0]["records"]
    cname_record = get_record(records, "CNAME")
    cname_record_id = cname_record["id"]
    data = {
        "zone": "company.com",
        "owner": "www",
        "rtype": "CNAME",
        "rdata": "company.com.",
        "ttl": "3600",
    }
    res = client.put(
        f"{settings.API_V2_STR}/records{cname_record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()

    assert edit_record_data["code"] == 409
    assert edit_record_data["message"] == "record already exists"


def test_edit_record_with_ttl_change(client: TestClient, api_key: str, mocker):
    """Test editing record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Edit a record with the different TTL
    - Query the db to assure it's edited
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
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    # edit record
    records = list_record_data["data"][0]["records"]
    cname_record = get_record(records, "CNAME")
    cname_record_id = cname_record["id"]
    data = {
        "zone": "company.com",
        "owner": "www",
        "rtype": "CNAME",
        "rdata": "company.com.",
        "ttl": "300",
    }
    res = client.put(
        f"{settings.API_V2_STR}/records{cname_record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    records = list_record_data["data"][0]["records"]
    edited_record_data = get_record(records, "CNAME")

    assert edit_record_data["code"] == 200
    assert edit_record_data["data"]["ttl"] == "300"

    assert list_record_data["code"] == 200
    _ttl = ttl_db.get(edited_record_data["ttl_id"])
    assert _ttl["ttl"] == "300"


def test_delete_record(client: TestClient, api_key: str, mocker):
    """Test deleting record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - List the default records
    - Delete one of the record
    - Query the db to assure it's deleted
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
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    # edit record
    records = list_record_data["data"][0]["records"]
    cname_record = get_record(records, "CNAME")
    cname_record_id = cname_record["id"]
    delete_res = client.delete(
        f"{settings.API_V2_STR}/record/delete/{cname_record_id}", headers=headers
    )
    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    records = list_record_data["data"][0]["records"]

    assert delete_res.status_code == 204
    # it must be 3 after deletion
    assert len(records) == 3


def test_edit_record_no_ttl_change_MX(client: TestClient, api_key: str, mocker):
    """Test editing record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add MX record
    - Edit a record with the same TTL
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
        "owner": "mx1",
        "rtype": "MX",
        "rdata": "10 mail.example.com.",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    json_data = res.json()
    record_id = json_data["data"]["id"]

    # edit record
    data = {
        "zone": "company.com",
        "owner": "mx1",
        "rtype": "MX",
        "rdata": "10 mail.example.com.",
        "ttl": 7200,
    }

    res = client.put(
        f"{settings.API_V2_STR}/records{record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()

    assert edit_record_data["code"] == 409
    assert edit_record_data["message"] == "record already exists"


def test_edit_record_with_ttl_change_MX(client: TestClient, api_key: str, mocker):
    """Test editing record from its endpoint.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Add MX record
    - Edit a record with the different TTL
    - Query the db to assure it's edited
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
        "owner": "mx1",
        "rtype": "MX",
        "rdata": "10 mail.example.com.",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    json_data = res.json()
    record_id = json_data["data"]["id"]

    # edit record
    data = {
        "zone": "company.com",
        "owner": "mx1",
        "rtype": "MX",
        "rdata": "10 mail.example.com.",
        "ttl": 14400,
    }
    res = client.put(
        f"{settings.API_V2_STR}/records{record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()

    # list record
    res = client.get(f"{settings.API_V2_STR}/domains", headers=headers)
    list_record_data = res.json()
    records = list_record_data["data"][0]["records"]
    edited_record_data = get_record(records, "MX")

    assert edit_record_data["code"] == 200
    assert edit_record_data["data"]["ttl"] == "14400"

    assert list_record_data["code"] == 200
    _ttl = ttl_db.get(edited_record_data["ttl_id"])
    assert _ttl["ttl"] == "14400"


def test_edit_record_respect_zone_limit(
    client: TestClient, api_key: str, monkeypatch, mocker
):
    """Test edit record respecting zone limit of 99

    - Create a User
    - Create a domain (with default SOA, NS, CNAME created)
    - Add TXT record
    - Edit a record with the different TXT value until it reaches a limit
    - Edit a record with tomorrows date
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
        "owner": "txt1",
        "rtype": "TXT",
        "rdata": "0",
        "ttl": 7200,
    }
    res = client.post(f"{settings.API_V2_STR}/records", json=data, headers=headers)
    json_data = res.json()
    record_id = json_data["data"]["id"]

    increment_serial = 0
    # 50 times for edit record is enough to make serial > 99
    # record edit increment serial twice at time
    while increment_serial < 50:
        data = {
            "zone": "company.com",
            "owner": "txt1",
            "rtype": "TXT",
            "rdata": f"{increment_serial}",
            "ttl": 7200,
        }
        res = client.put(
            f"{settings.API_V2_STR}/records{record_id}", json=data, headers=headers
        )
        edit_record_data = res.json()

        increment_serial += 1

    assert edit_record_data["code"] == 429
    assert edit_record_data["message"] == "zone change limit reached"

    # ensure correct serial
    serial = record_api.get_soa_serial("company.com")
    today_date = helpers.soa_time_set()

    record_date = serial[:-2]
    serial_counter = serial[-2:]

    assert serial_counter == "98"
    assert record_date == today_date
    assert serial == f"{today_date}98"

    #
    # if user waits until tomorrow
    #
    def fake_soa_time_set():
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
        return tomorrow_date.strftime("%Y%m%d")

    monkeypatch.setattr(helpers, "soa_time_set", fake_soa_time_set)
    data = {
        "zone": "company.com",
        "owner": "txt1",
        "rtype": "TXT",
        "rdata": "random text",
        "ttl": 7200,
    }
    res = client.put(
        f"{settings.API_V2_STR}/records{record_id}", json=data, headers=headers
    )
    edit_record_data = res.json()

    assert edit_record_data["code"] == 200

    # ensure correct serial
    serial = record_api.get_soa_serial("company.com")
    today_date = helpers.soa_time_set()

    record_date = serial[:-2]
    serial_counter = serial[-2:]

    assert serial_counter == "03"
    assert record_date == today_date
    assert serial == f"{today_date}03"
