from fastapi.testclient import TestClient

from app.core.config import settings


def test_health(client: TestClient):
    res = client.get(f"{settings.API_V2_STR}/health")
    data = res.json()

    assert "100" in data["data"]["check"]
