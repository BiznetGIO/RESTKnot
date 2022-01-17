from typing import List

from fastapi.testclient import TestClient

import app.helpers.producer  # pylint: disable=wrong-import-order
import app.tests.fixtures.messages as message_fixture
from app.core.config import settings

_messages: List[str] = []


def fake_send(messages):
    _messages.append(messages)


def test_messages(client: TestClient, api_key: str, monkeypatch, mocker):
    """Test if the command sent to broker created appropriately.

    - Create a User
    - Create a domain (with default SOA,NS,CNAME created)
    - Assert the sent command
    """
    mocker.patch("app.helpers.producer.kafka_producer")
    monkeypatch.setattr(app.helpers.producer, "send", fake_send)
    headers = {"X-Api-Key": api_key}

    # create user
    data = {"email": "first@company.com"}
    post_res = client.post(f"{settings.API_V2_STR}/users/", json=data, headers=headers)
    json_data = post_res.json()
    user_id = json_data["data"]["id"]

    # add domain
    data = {"zone": "company.com", "user_id": user_id}
    client.post(f"{settings.API_V2_STR}/domains", json=data, headers=headers)

    # messages: 4 if using `set_default_zone`, 7 if using `set_zone`
    assert len(_messages) == 7
    # they should be ordered like this, otherwise knot will fail to create
    # configs or zones
    assert _messages[0]["knot"][1] == message_fixture.knot_conf_set
    assert _messages[1]["knot"][1] == message_fixture.knot_zone_set_soa
    assert _messages[2]["knot"][1] == message_fixture.knot_zone_set_ns
