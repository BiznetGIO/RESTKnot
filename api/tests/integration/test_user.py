class TestUser:
    def test_list_no_user(self, client):
        headers = {"X-Api-Key": "123"}
        res = client.get("/api/user/list", headers=headers)
        json_data = res.get_json()

        assert json_data["code"] == 404

    def test_crate_user(self, client):
        headers = {"X-Api-Key": "123"}
        data = {"email": "test-one@company.com"}
        res = client.post("/api/user/add", data=data, headers=headers)
        json_data = res.get_json()

        assert json_data["code"] == 201
        assert json_data["data"]["email"] == "test-one@company.com"

    def test_edit_user(self, client):
        headers = {"X-Api-Key": "123"}
        data = {"email": "test-one@company.com"}
        res = client.post("/api/user/add", data=data, headers=headers)
        json_data = res.get_json()

        assert json_data["code"] == 201
        assert json_data["data"]["email"] == "test-one@company.com"
