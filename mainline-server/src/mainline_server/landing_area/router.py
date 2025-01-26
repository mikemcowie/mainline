from fastapi import APIRouter, Request

from mainline_server.rest_schema import APIResource, BaseResource
from mainline_server.rest_utils import provide_hyperlink

router = APIRouter()


class HomePage(BaseResource):
    pass


@router.get("/", response_model=APIResource[HomePage])
def api_root(request: Request):
    return APIResource(
        self=provide_hyperlink(request, "Home", "api_root"),
        title="Home",
        object={},
        links=[],
    )
