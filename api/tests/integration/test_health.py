class TestHealth:
    def test_health(self, client):
        res = client.get("/api/health")
        data = res.get_json()

        assert "running" in data["data"]["status"]
