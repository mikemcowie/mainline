from typing import Annotated

from fastapi import Form, Request, status
from fastapi.responses import RedirectResponse
from hyperapi import APIRouter
from hyperapi.rest_schema import APILink, APILinkAction, APIResource
from hyperapi.rest_utils import meta, negotiated, provide_hyperlink

from mainline_server.landing_area.components import (
    COPY,
    HomePage,
    HomePageCopy,
    HomePageEnquiryComponent,
    HomePageEnquiryForm,
    HomePageEnquiryResponse,
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


@router.post("/enquiries", response_model=HomePageEnquiryResponse)
def enquire(request: Request, enquiry: Annotated[HomePageEnquiryForm, Form()]):
    return RedirectResponse(
        url=str(provide_hyperlink(request, "Enquiry result", "enquiry_result").href),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/enquiries/mine", response_model=HomePageEnquiryResponse)
def enquiry_result(request: Request):
    return negotiated(
        request,
        HomePageEnquiryComponent(
            resource=HomePageEnquiryResponse(
                self=provide_hyperlink(request, "Home", "api_root"),
                title="Foo",  # enquiry.github_repository,
                object={},
                links=[],
                meta=meta(request.app),
            ),
            children=[],
        ),
    )
