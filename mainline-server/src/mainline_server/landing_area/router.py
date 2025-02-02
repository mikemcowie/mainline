from fastapi import APIRouter, Request

from mainline_server.landing_area.components import (
    COPY,
    HomePage,
    HomePageCopy,
    HomePageResource,
)
from mainline_server.rest_schema import APIResource
from mainline_server.rest_utils import meta, negotiated, provide_hyperlink

router = APIRouter()


@router.get("/", response_model=HomePageResource)
def api_root(request: Request):
    """The home page, initial landing spot"""
    return negotiated(
        request,
        HomePage(
            resource=APIResource(
                self=provide_hyperlink(request, "Home", "api_root"),
                meta=meta(request.app),
                title="Home",
                object=HomePageCopy(heading=COPY.HEADING, detail=COPY.DETAIL),
                links=[],
            ),
            children=[],
        ),
    )
