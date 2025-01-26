from fastapi import status
from fastapi.testclient import TestClient


def test_home(client: TestClient):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["self"]["href"] == str(client.base_url) + "/"


def test_home_html(client: TestClient):
    res = client.get("/", headers={"accept": "text/html"})
    assert res.status_code == status.HTTP_200_OK
    assert "<html>" in res.text
    assert "text/html" in res.headers.get("content-type")


def test_home_plain(client: TestClient):
    res = client.get("/", headers={"accept": "text/plain"})
    assert res.status_code == status.HTTP_406_NOT_ACCEPTABLE
