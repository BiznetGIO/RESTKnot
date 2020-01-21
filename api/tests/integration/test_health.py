class TestHealth:
    def test_health(self, client):
        res = client.get("/api/health")
        data = res.get_json()

        assert "100" in data["data"]["check"]
