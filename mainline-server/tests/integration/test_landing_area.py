from fastapi import status
from fastapi.testclient import TestClient


def test_home(client: TestClient):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["self"]["href"] == str(client.base_url) + "/"
