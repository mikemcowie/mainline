from unittest import mock

import pytest
from typer.testing import CliRunner

from mainline_server.cli import app


@pytest.fixture(autouse=True)
def uvicorn_run():
    with mock.patch("mainline_server.cli.uvicorn.run") as uvicorn_run:
        yield uvicorn_run


def test_uvicorn_called_with_dev_options_if_dev_cli(uvicorn_run: mock.MagicMock):
    result = CliRunner().invoke(app, ["--dev"])
    assert result.exception is None
    assert result.exit_code == 0
    uvicorn_run.assert_called_once_with(
        app="mainline_server.api:dev_app", port=mock.ANY, host="0.0.0.0", reload=True
    )


def test_uvicorn_called_with_dev_options_if_prod_cli(uvicorn_run: mock.MagicMock):
    result = CliRunner().invoke(app, [])
    assert result.exception is None
    assert result.exit_code == 0
    uvicorn_run.assert_called_once_with(
        app="mainline_server.api:prod_app", port=8000, workers=mock.ANY, host="0.0.0.0"
    )


def test_uvicorn_cannot_be_called_with_workers_and_dev(uvicorn_run: mock.MagicMock):
    result = CliRunner().invoke(app, ["--dev", "--workers", "2"])
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code != 0
