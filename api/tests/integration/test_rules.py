class TestCNAMERules:
    def test_duplicate_record(self, client, mocker):
        """Create multiple CNAME record with same owner and rdata.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - # default CNAME owner is `www`
        - Add CNAME record with `www` as owner -> must be FAIL (duplicate record)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
            "rdata": "company.com.",
            "ttl": 3600,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 409
        assert add_record_data["message"] == "The record already exists"

    def test_possible_duplicate_record(self, client, mocker):
        """Edit CNAME record that possible same with other.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - # default CNAME owner is `www`
        - Add CNAME record with `www1` as owner.
        - Edit CNAME record with `wwww` as owner and `company.com.` as rdata -> must be FAIL (duplicate record)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
            "rdata": "company.com.",
            "ttl": 3600,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        json_data = res.get_json()
        record_id = json_data["data"]["id"]

        # edit possible duplicate record
        data = {
            "zone": "company.com",
            "owner": "www",
            "rtype": "CNAME",
            "rdata": "company.com.",
            "ttl": 3600,
        }
        res = client.put(f"/api/record/edit/{record_id}", data=data, headers=headers)
        edit_record_data = res.get_json()

        assert edit_record_data["code"] == 409
        assert edit_record_data["message"] == "The record already exists"

    def test_unique_host(self, client, mocker):
        """Create multiple CNAME record with different owner/host.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - # default CNAME owner is `www`
        - Add CNAME record with `www1` as owner -> must be SUCCESS (unique allowed)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
        """Create multiple CNAME record with same owner/host.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - # default CNAME owner is `www`
        - Add CNAME record with `www` as owner -> must be FAIL (duplicate owner)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
        """Create CNAME record with same A owner.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add A record with `host` as owner
        - Add CNAME record with `host` as owner -> must be FAIL (clash with A owner)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
    def test_duplicate_record(self, client, mocker):
        """Create multiple A record with same owner and rdata.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add A record with `a1` as owner and `1.1.1.1` as rdata
        - Add A record with `a1` as owner and `1.1.1.1` as rdata -> must be FAIL (duplicate record)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
            "owner": "a1",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        client.post("/api/record/add", data=data, headers=headers)

        # add duplicate record
        data = {
            "zone": "company.com",
            "owner": "a1",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()

        assert add_record_data["code"] == 409
        assert add_record_data["message"] == "The record already exists"

    def test_possible_duplicate_record(self, client, mocker):
        """Edit A record that possible same with other.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add A record with `a1` as owner and `1.1.1.1` as rdata
        - Add A record with `a1` as owner and `2.2.2.2` as rdata
        - Edit A record with `a1` as owner and `1.1.1.1` as rdata -> must be FAIL (duplicate record)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
            "owner": "a1",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        client.post("/api/record/add", data=data, headers=headers)

        # add record
        data = {
            "zone": "company.com",
            "owner": "a1",
            "rtype": "A",
            "rdata": "2.2.2.2",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        json_data = res.get_json()
        record_id = json_data["data"]["id"]

        # edit possible duplicate record
        data = {
            "zone": "company.com",
            "owner": "a1",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        res = client.put(f"/api/record/edit/{record_id}", data=data, headers=headers)
        edit_record_data = res.get_json()

        assert edit_record_data["code"] == 409
        assert edit_record_data["message"] == "The record already exists"

    def test_not_unique_owner(self, client, mocker):
        """Create A record with same owner.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add A record with `host` as owner
        - Add A record with `host` as owner -> must be SUCCESS (same owner allowed)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
        """Create A record with same CNAME owner.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add CNAME record with `host` as owner
        - Add A record with `host` as owner -> must be FAIL (clash with CNAME owner)
        """
        mocker.patch("app.helpers.producer.kafka_producer")
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
