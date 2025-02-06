from typing import Annotated

from fastapi import Form, Request
from hyperapi import APIRouter, HyperAPI
from hyperapi.rest_schema import APILink, APILinkAction, APIResource
from hyperapi.rest_utils import meta, negotiated, provide_hyperlink

from mainline_server.landing_area.components import (
    COPY,
    HomePage,
    HomePageCopy,
    HomePageEnquiryForm,
    HomePageResource,
)

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
                links=[
                    APILink(
                        href=str(request.url_for("enquire")),
                        name="enquire",
                        actions=[
                            APILinkAction(
                                method="POST",
                                title="Check my project",
                                description=None,
                                highlight=True,
                                json_schema=HomePageEnquiryForm.model_json_schema(),
                            )
                        ],
                    )
                ],
            ),
            children=[],
        ),
    )


@router.get("/enquiries/")
def enquire_get(request: Request):
    assert isinstance(request.app, HyperAPI)
    for route in request.app.routes:
        if "enquiries" in str(route):
            print(route.endpoint)


@router.post("/enquiries/")
def enquire(request: Request, enquiry: Annotated[HomePageEnquiryForm, Form()]):
    pass
