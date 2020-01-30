class TestFunctional:
    def test_create_domain(self, client):
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

        assert create_domain_data["code"] == 201
        assert create_domain_data["data"]["zone"] == "company.com"
        assert list_domain_data["code"] == 200
        assert list_domain_data["data"][0]["zone"] == "company.com"
        # 4: SOA, NS, NS, CNAME
        assert len(list_domain_data["data"][0]["records"]) == 4
