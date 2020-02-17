import app.helpers.producer


class TestDomain:
    def test_list_no_domain(self, client):
        """Test if db contains no domain."""
        headers = {"X-Api-Key": "123"}
        res = client.get("/api/domain/list", headers=headers)
        json_data = res.get_json()

        assert json_data["code"] == 404

    def test_domain(self, client, mocker):
        """Test domain happy path.

        - Create a User
        - Create a domain (with default SOA,NS,CNAME created)
        - List the domain
        - Delete the domain
        """
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
        # list domain
        res = client.get("/api/domain/list", headers=headers)
        list_domain_data = res.get_json()
        # delete domain
        data = {"zone": "company.com"}
        delete_domain_data = client.delete(
            "/api/domain/delete", data=data, headers=headers
        )

        assert create_domain_data["code"] == 201
        assert create_domain_data["data"]["zone"] == "company.com"
        assert list_domain_data["code"] == 200
        assert list_domain_data["data"][0]["zone"] == "company.com"
        # 4: SOA, NS, NS, CNAME
        assert len(list_domain_data["data"][0]["records"]) == 4
        # TODO can we assert the result of `call_args` since using `call_with`
        # is not feasible way knowing the very long arguments

        # 4: set_config, set_zone, delegate, delegate (creation)
        # 5: unset_config, unset_zone (SOA, NS, NS, CNAME)
        assert app.helpers.producer.send.call_count == 9
        assert delete_domain_data.status_code == 204
