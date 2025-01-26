from fastapi import status
from fastapi.testclient import TestClient


def test_health(client: TestClient):
    res = client.get("/health")
    assert res.status_code == status.HTTP_200_OK
    assert res.text == "pass"
