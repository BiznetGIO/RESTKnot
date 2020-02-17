class TestCNAMERules:
    def test_unique_host(self, client, mocker):
        mocker.patch("app.helpers.helpers.check_producer")
        mocker.patch("app.helpers.producer.send")

        headers = {"X-Api-Key": "123"}

        # create user
        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        # add domain
        data = {"zone": "company.com", "user_id": user_id}
        client.post("/api/domain/add", data=data, headers=headers)
        # add record
        data = {
            "zone": "company.com",
            "owner": "www1",
            "rtype": "CNAME",
            "rdata": "company.com",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 201
        assert add_record_data["data"]["type"] == "CNAME"
        assert add_record_data["data"]["owner"] == "www1"

    def test_not_unique_host(self, client, mocker):
        mocker.patch("app.helpers.helpers.check_producer")
        mocker.patch("app.helpers.producer.send")
        headers = {"X-Api-Key": "123"}

        # create user
        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        # add domain
        data = {"zone": "company.com", "user_id": user_id}
        client.post("/api/domain/add", data=data, headers=headers)
        # add record
        data = {
            "zone": "company.com",
            "owner": "www",
            "rtype": "CNAME",
            "rdata": "company.com",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 409
        assert (
            add_record_data["message"] == "A CNAME record already exist with that owner"
        )

    def test_clash_with_A_owner(self, client, mocker):
        mocker.patch("app.helpers.helpers.check_producer")
        mocker.patch("app.helpers.producer.send")
        headers = {"X-Api-Key": "123"}

        # create user
        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        # add domain
        data = {"zone": "company.com", "user_id": user_id}
        client.post("/api/domain/add", data=data, headers=headers)
        # add record A
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        client.post("/api/record/add", data=data, headers=headers)
        # add record
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "CNAME",
            "rdata": "company.com",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 409
        assert add_record_data["message"] == "An A record already exist with that owner"


class TestARules:
    def test_not_unique_owner(self, client, mocker):
        mocker.patch("app.helpers.helpers.check_producer")
        mocker.patch("app.helpers.producer.send")
        headers = {"X-Api-Key": "123"}

        # create user
        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        # add domain
        data = {"zone": "company.com", "user_id": user_id}
        client.post("/api/domain/add", data=data, headers=headers)
        # add record A
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        # add record A
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "A",
            "rdata": "2.2.2.2",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 201
        assert add_record_data["data"]["type"] == "A"
        assert add_record_data["data"]["owner"] == "host"

    def test_clash_with_cname_owner(self, client, mocker):
        mocker.patch("app.helpers.helpers.check_producer")
        mocker.patch("app.helpers.producer.send")
        headers = {"X-Api-Key": "123"}

        # create user
        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        # add domain
        data = {"zone": "company.com", "user_id": user_id}
        client.post("/api/domain/add", data=data, headers=headers)
        # add record CNAME
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "CNAME",
            "rdata": "company.com",
            "ttl": 7200,
        }
        client.post("/api/record/add", data=data, headers=headers)
        # add record A
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 409
        assert (
            add_record_data["message"] == "A CNAME record already exist with that owner"
        )
