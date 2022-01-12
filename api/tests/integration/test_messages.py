from typing import List

import tests.fixtures.messages as message_fixture

import app.helpers.producer


class TestMessages:
    _messages: List[str] = []

    def fake_send(self, messages):
        self._messages.append(messages)

    def test_messages(self, client, monkeypatch, mocker):
        """Test if the command sent to broker created appropriately.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Assert the sent command
        """
        mocker.patch("app.helpers.producer.kafka_producer")
        monkeypatch.setattr(app.helpers.producer, "send", self.fake_send)
        headers = {"X-Api-Key": "123"}

        # create user
        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        # add domain
        data = {"zone": "company.com", "user_id": user_id}
        client.post("/api/domain/add", data=data, headers=headers)

        assert len(self._messages) == 4
        # they should be ordered like this, otherwise knot will fail to create
        # configs or zones
        assert self._messages[0]["knot"][1] == message_fixture.knot_conf_set
        assert self._messages[1]["knot"][2] == message_fixture.knot_zone_set_ns
        assert self._messages[2]["knot"][1] == message_fixture.knot_delegate_file
