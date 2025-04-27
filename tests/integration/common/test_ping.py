from fastapi.testclient import TestClient


def test_ping(client: TestClient):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == "Pong!"
