from pathlib import Path

import structlog
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from mainline_server import NAME
from mainline_server.landing_area.router import router as landing_area_router

logger = structlog.get_logger()


def app_factory(
    dev: bool = False, htmlcov_dir: Path = Path(__file__).parents[2] / "htmlcov"
):
    api = FastAPI(title=NAME)

    @api.get("/health", status_code=status.HTTP_200_OK)
    def health():
        return PlainTextResponse("pass")

    api.include_router(landing_area_router)

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
