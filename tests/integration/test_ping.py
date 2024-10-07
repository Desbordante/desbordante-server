from fastapi.testclient import TestClient


def test_retrieve_task(client: TestClient):
    response = client.get("api/common/ping")

    assert response.status_code == 200
    assert response.json() == "Pong!"
