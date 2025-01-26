from pathlib import Path

import structlog
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

logger = structlog.get_logger()


def app_factory(
    dev: bool = False, htmlcov_dir: Path = Path(__file__).parents[2] / "htmlcov"
):
    api = FastAPI()

    @api.get("/health", status_code=status.HTTP_200_OK)
    def health():
        return PlainTextResponse("pass")

    if dev:
        # As a development convenience
        # We host the htmlcov directory
        logger.info("running development mode, so including coverage static files")
        if not htmlcov_dir.exists():
            htmlcov_dir.mkdir(exist_ok=True)
        api.mount(
            "/htmlcov", StaticFiles(directory=htmlcov_dir, html=True), name="htmlcov"
        )

    return api


dev_app = app_factory(dev=True)
prod_app = app_factory()
