class TestUser:
    def test_list_no_user(self, client):
        headers = {"X-Api-Key": "123"}
        res = client.get("/api/user/list", headers=headers)
        json_data = res.get_json()

        assert json_data["code"] == 404

    def test_crate_user(self, client, clean_users):
        headers = {"X-Api-Key": "123"}

        data = {"email": "first@company.com"}
        res = client.post("/api/user/add", data=data, headers=headers)
        response_data = res.get_json()

        res = client.get("/api/user/list", headers=headers)
        db_data = res.get_json()
        clean_users()

        # assert response
        assert response_data["code"] == 201
        assert response_data["data"]["email"] == "first@company.com"
        # assert db value
        assert "first@company.com" in db_data["data"][0].values()

    def test_edit_user(self, client, clean_users):
        headers = {"X-Api-Key": "123"}

        data = {"email": "first@company.com"}
        res = client.post("/api/user/add", data=data, headers=headers)
        json_data = res.get_json()
        user_id = json_data["data"]["id"]

        data = {"email": "first_edited@company.com"}
        res = client.put(f"/api/user/edit/{user_id}", data=data, headers=headers)
        res_data = res.get_json()

        res = client.get("/api/user/list", headers=headers)
        db_data = res.get_json()
        clean_users()

        assert res_data["code"] == 200
        assert res_data["data"]["email"] == "first_edited@company.com"
        assert "first_edited@company.com" in db_data["data"][0].values()

    def test_delete_user(self, client, clean_users):
        headers = {"X-Api-Key": "123"}

        data = {"email": "first@company.com"}
        post_res = client.post("/api/user/add", data=data, headers=headers)
        json_data = post_res.get_json()
        user_id = json_data["data"]["id"]

        delete_res = client.delete(f"/api/user/delete/{user_id}", headers=headers)

        res = client.get("/api/user/list", headers=headers)
        db_data = res.get_json()
        clean_users()

        assert delete_res.status_code == 204
        assert db_data["code"] == 404
