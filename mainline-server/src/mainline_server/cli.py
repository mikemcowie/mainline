"""Provides the app's entrypoints"""

import sys

import structlog
import typer
import uvicorn

app = typer.Typer(no_args_is_help=True)
logger = structlog.get_logger()


@app.command()
def api(dev: bool = False, workers: int | None = None, port: int = 8000):
    """Run the main API process"""
    if workers and dev:
        logger.error("Cannot select both --dev and --workers")
        sys.exit(1)
    if dev:
        uvicorn.run(
            app="mainline_server.api:dev_app", port=port, host="0.0.0.0", reload=True
        )
    else:
        uvicorn.run(
            app="mainline_server.api:prod_app",
            port=port,
            workers=workers,
            host="0.0.0.0",
        )


def go():  # pragma: no cover
    """The primary entrypoint for the server"""
    app()
