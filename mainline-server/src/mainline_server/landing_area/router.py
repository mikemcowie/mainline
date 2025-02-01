from fastapi import APIRouter, Request

from mainline_server.rest_schema import APIResource, BaseResource
from mainline_server.rest_utils import meta, negotiated, provide_hyperlink

router = APIRouter()


class HomePage(BaseResource):
    pass


@router.get("/", response_model=APIResource[HomePage])
def api_root(request: Request):
    """The home page, initial landing spot"""
    return negotiated(
        request,
        APIResource(
            self=provide_hyperlink(request, "Home", "api_root"),
            meta=meta(request.app),
            title="Home",
            object={},
            links=[],
        ),
    )
