import datetime

import app.helpers.helpers


class TestRecord:
    def get_record(self, records, type_):
        for record in records:
            if record["type"] == type_:
                return record

    def test_list_no_Record(self, client):
        """Test if db contains no record."""
        headers = {"X-Api-Key": "123"}
        res = client.get("/api/domain/list", headers=headers)
        json_data = res.get_json()

        assert json_data["code"] == 404

    def test_add_record(self, client, mocker):
        """Test adding record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add a record
        - Query the db to assure it's created
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
        res = client.post("/api/domain/add", data=data, headers=headers)
        create_domain_data = res.get_json()
        # add record
        data = {
            "zone": "company.com",
            "owner": "host",
            "rtype": "A",
            "rdata": "1.1.1.1",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        add_record_data = res.get_json()
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()

        assert create_domain_data["code"] == 201
        assert create_domain_data["data"]["zone"] == "company.com"

        assert add_record_data["code"] == 201
        assert add_record_data["data"]["owner"] == "host"
        assert add_record_data["data"]["rdata"] == "1.1.1.1"

        assert list_record_data["code"] == 200
        assert list_record_data["data"][0]["zone"] == "company.com"
        assert list_record_data["data"][0]["user"]["email"] == "first@company.com"

    def test_edit_record(self, client, mocker):
        """Test editing record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add a record
        - Edit a record
        - Query the db to assure it's edited
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
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        # edit record
        records = list_record_data["data"][0]["records"]
        cname_record = self.get_record(records, "CNAME")
        cname_record_id = cname_record["id"]
        data = {
            "zone": "company.com",
            "owner": "www_edit",
            "rtype": "CNAME",
            "rdata": "company_edited.com",
            "ttl": 3600,
        }
        res = client.put(
            f"/api/record/edit/{cname_record_id}", data=data, headers=headers
        )
        edit_record_data = res.get_json()
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        records = list_record_data["data"][0]["records"]
        edited_record_data = self.get_record(records, "CNAME")

        assert edit_record_data["code"] == 200
        assert edit_record_data["data"]["owner"] == "www_edit"

        assert list_record_data["code"] == 200
        assert edited_record_data["rdata"] == "company_edited.com"

    def test_edit_record_no_ttl_change(self, client, mocker):
        """Test editing record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Edit a record with the same TTL
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
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        # edit record
        records = list_record_data["data"][0]["records"]
        cname_record = self.get_record(records, "CNAME")
        cname_record_id = cname_record["id"]
        data = {
            "zone": "company.com",
            "owner": "www",
            "rtype": "CNAME",
            "rdata": "company.com.",
            "ttl": "3600",
        }
        res = client.put(
            f"/api/record/edit/{cname_record_id}", data=data, headers=headers
        )
        edit_record_data = res.get_json()

        assert edit_record_data["code"] == 409
        assert edit_record_data["message"] == "The record already exists"

    def test_edit_record_with_ttl_change(self, client, mocker):
        """Test editing record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Edit a record with the different TTL
        - Query the db to assure it's edited
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
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        # edit record
        records = list_record_data["data"][0]["records"]
        cname_record = self.get_record(records, "CNAME")
        cname_record_id = cname_record["id"]
        data = {
            "zone": "company.com",
            "owner": "www",
            "rtype": "CNAME",
            "rdata": "company.com.",
            "ttl": "300",
        }
        res = client.put(
            f"/api/record/edit/{cname_record_id}", data=data, headers=headers
        )
        edit_record_data = res.get_json()
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        records = list_record_data["data"][0]["records"]
        edited_record_data = self.get_record(records, "CNAME")

        assert edit_record_data["code"] == 200
        assert edit_record_data["data"]["ttl"] == "300"

        assert list_record_data["code"] == 200
        assert edited_record_data["ttl"] == "300"

    def test_delete_record(self, client, mocker):
        """Test deleting record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - List the default records
        - Delete one of the record
        - Query the db to assure it's deleted
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
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        # edit record
        records = list_record_data["data"][0]["records"]
        cname_record = self.get_record(records, "CNAME")
        cname_record_id = cname_record["id"]
        delete_res = client.delete(
            f"/api/record/delete/{cname_record_id}", headers=headers
        )
        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        records = list_record_data["data"][0]["records"]

        assert delete_res.status_code == 204
        # it must be 3 after deletion
        assert len(records) == 3

    def test_edit_record_no_ttl_change_MX(self, client, mocker):
        """Test editing record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add MX record
        - Edit a record with the same TTL
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
            "owner": "mx1",
            "rtype": "MX",
            "rdata": "10 mail.example.com.",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        json_data = res.get_json()
        record_id = json_data["data"]["id"]

        # edit record
        data = {
            "zone": "company.com",
            "owner": "mx1",
            "rtype": "MX",
            "rdata": "10 mail.example.com.",
            "ttl": 7200,
        }

        res = client.put(f"/api/record/edit/{record_id}", data=data, headers=headers)
        edit_record_data = res.get_json()

        assert edit_record_data["code"] == 409
        assert edit_record_data["message"] == "The record already exists"

    def test_edit_record_with_ttl_change_MX(self, client, mocker):
        """Test editing record from its endpoint.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - Add MX record
        - Edit a record with the different TTL
        - Query the db to assure it's edited
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
            "owner": "mx1",
            "rtype": "MX",
            "rdata": "10 mail.example.com.",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        json_data = res.get_json()
        record_id = json_data["data"]["id"]

        # edit record
        data = {
            "zone": "company.com",
            "owner": "mx1",
            "rtype": "MX",
            "rdata": "10 mail.example.com.",
            "ttl": 14400,
        }
        res = client.put(f"/api/record/edit/{record_id}", data=data, headers=headers)
        edit_record_data = res.get_json()

        # list record
        res = client.get("/api/domain/list", headers=headers)
        list_record_data = res.get_json()
        records = list_record_data["data"][0]["records"]
        edited_record_data = self.get_record(records, "MX")

        assert edit_record_data["code"] == 200
        assert edit_record_data["data"]["ttl"] == "14400"

        assert list_record_data["code"] == 200
        assert edited_record_data["ttl"] == "14400"

    def test_edit_record_respect_zone_limit(self, client, monkeypatch, mocker):
        """Test edit record respecting zone limit of 99

        - Create a User
        - Create a domain (with default SOA, NS, CNAME created)
        - Add TXT record
        - Edit a record with the different TXT value until it reaches a limit
        - Edit a record with tomorrows date
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
            "owner": "txt1",
            "rtype": "TXT",
            "rdata": "0",
            "ttl": 7200,
        }
        res = client.post("/api/record/add", data=data, headers=headers)
        json_data = res.get_json()
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
                f"/api/record/edit/{record_id}", data=data, headers=headers
            )
            edit_record_data = res.get_json()

            increment_serial += 1

        assert edit_record_data["code"] == 429
        assert edit_record_data["message"] == "Zone Change Limit Reached"

        # if user waits until tomorrow
        def fake_soa_time_set():
            tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
            return tomorrow_date.strftime("%Y%m%d")

        monkeypatch.setattr(app.helpers.helpers, "soa_time_set", fake_soa_time_set)
        data = {
            "zone": "company.com",
            "owner": "txt1",
            "rtype": "TXT",
            "rdata": "random text",
            "ttl": 7200,
        }
        res = client.put(f"/api/record/edit/{record_id}", data=data, headers=headers)
        edit_record_data = res.get_json()

        assert edit_record_data["code"] == 200
