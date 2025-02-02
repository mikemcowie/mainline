from enum import StrEnum
from functools import cache
from typing import Mapping

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from mainline_server import AUTHOR, KEYWORDS
from mainline_server.rest_schema import (
    APILink,
    MetaCharset,
    MetaHTMLEquivContent,
    MetaNameContent,
    MetaUnion,
)
from mainline_server.ui.components.layout import Column, Component, Container, Row
from mainline_server.ui.components.page import DocumentHead, Page
from mainline_server.ui.render import render


class ContentType(StrEnum):
    JSON = "application/json"
    HTML = "text/html"
    PLAINTEXT = "text/plain"


@cache
def meta(app: FastAPI) -> tuple[MetaUnion, ...]:
    """Provides meta items of a response"""
    allowed_remotes = [r.src for r in DocumentHead.scripts] + [
        r.href for r in DocumentHead.stylesheets
    ]
    return (
        MetaCharset(charset="UTF-8"),
        # sane httpquivcontent per https://www.w3schools.com/tags/att_meta_http_equiv.asp
        MetaHTMLEquivContent(
            http_equiv="content-security-policy",
            content=f"default-src 'self' {' '.join(allowed_remotes)}",
        ),
        MetaNameContent(name="application-name", content=app.title),
        MetaNameContent(name="author", content=AUTHOR),
        MetaNameContent(name="description", content=app.description),
        MetaNameContent(name="generator", content=app.title),
        MetaNameContent(name="keywords", content=", ".join(KEYWORDS)),
        MetaNameContent(
            name="viewport", content="width=device-width, initial-scale=1.0"
        ),
    )


def allowable_content_types(headers: Mapping[str, str]) -> list[ContentType]:
    """A rudimentory content negotiation processor

    roughly as guided by
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept

    It doesn't take into consideration weighting, and prefers
    HTML to JSON to Plaintext

    Except with wildcard accept, where it prefers JSON because
    wildcard accepts tends to get sent by programatic clients

    This should get replaced by a proper content negotiation
    system, but it's good enough for now.
    """
    accepts_header = headers.get("accept", "*/*")
    accepts: list[ContentType] = []
    if ContentType.HTML.value in accepts_header:
        accepts.append(ContentType.HTML)
    if ContentType.JSON.value in accepts_header:
        accepts.append(ContentType.JSON)
    if ContentType.PLAINTEXT.value in accepts_header:
        accepts.append(ContentType.PLAINTEXT)
    if accepts_header == "*/*":
        accepts = [a for a in ContentType]
    if accepts:
        return accepts
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"server accepts {[t.value for t in ContentType]}, got {accepts_header}",
    )


def provide_hyperlink(
    request: Request, name: str, target: str, **path_params
) -> APILink:
    """Provides APILink object to help add hypermedia to response objects"""
    return APILink(href=str(request.url_for(target, **path_params)), name=name)  # type: ignore


def negotiated(request: Request, main_component: Component):
    """Returns a negotiated response object"""
    preferred = allowable_content_types(request.headers)[0]
    if preferred == ContentType.JSON:
        # FastAPI itself will render the pydantic object
        # Into a response object
        return main_component.resource
    if preferred == ContentType.HTML:
        # render via the whole HTML rendering machinery
        # which is a whole other module to be designed still
        return HTMLResponse(
            str(
                render(
                    Page(
                        resource=main_component.resource,
                        children=[
                            Container(
                                id="root-container",
                                cls=["container-fluid", "h-100", "overflow-hidden"],
                                children=[
                                    Row(
                                        id="head-row",
                                        children=[
                                            Column(
                                                id="head-col-1", width=12, children=[]
                                            )
                                        ],
                                    ),
                                    Row(
                                        id="body-row",
                                        cls=["row", "min-vh-100"],
                                        children=[
                                            Column(
                                                id="body-col-1", width=4, children=[]
                                            ),
                                            Column(
                                                id="body-col-2",
                                                width=4,
                                                children=[main_component],
                                                cls=["col", "align-self-center"],
                                            ),
                                            Column(
                                                id="body-col-3", width=4, children=[]
                                            ),
                                        ],
                                    ),
                                    Row(
                                        id="footer-row",
                                        children=[
                                            Column(
                                                id="footer-col-1", width=12, children=[]
                                            )
                                        ],
                                    ),
                                ],
                            )
                        ],
                    )
                )
            )
        )
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="caannot find acceptable response type for accept header "
        "{request.headers.get('accept')}",
    )
