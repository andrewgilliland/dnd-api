from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_races():
    response = client.get("/api/v1/races")
    assert response.status_code == 200
    data = response.json()
    assert "races" in data
    assert isinstance(data["races"], list)
