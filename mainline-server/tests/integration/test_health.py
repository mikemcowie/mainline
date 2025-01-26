import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from mainline_server.api import app_factory


@pytest.fixture
def app():
    return app_factory(dev=True)


@pytest.fixture
def client(app: FastAPI):
    c = TestClient(app=app)
    with c:
        return c


def test_health(client: TestClient):
    res = client.get("/health")
    assert res.status_code == status.HTTP_200_OK
    assert res.text == "pass"
