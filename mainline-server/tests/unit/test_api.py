from pathlib import Path

from fastapi import FastAPI
from mainline_server import api
from starlette.routing import Mount


def get_staticfiles_apps(app: FastAPI):
    return [route.app for route in app.router.routes if isinstance(route, Mount)]


def test_dev_app_has_htmlcov():
    dev_mounts = get_staticfiles_apps(api.dev_app)
    prod_mounts = get_staticfiles_apps(api.prod_app)
    assert len(dev_mounts) == len(prod_mounts) + 1


def test_htmlcov_dir_created_if_not_exists(tmp_path: Path):
    htmlcov = tmp_path / "htmlcov"
    assert not htmlcov.exists()
    api.app_factory(dev=True, htmlcov_dir=tmp_path / "htmlcov")
    assert htmlcov.exists()
