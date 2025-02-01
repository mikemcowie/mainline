from enum import StrEnum
from functools import cache
from typing import Mapping

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse

from mainline_server import AUTHOR, KEYWORDS
from mainline_server.rest_schema import (
    APILink,
    APIResource,
    MetaCharset,
    MetaHTMLEquivContent,
    MetaNameContent,
    MetaUnion,
)
from mainline_server.ui.page import Page


class ContentType(StrEnum):
    JSON = "application/json"
    HTML = "text/html"
    PLAINTEXT = "text/plain"


@cache
def meta(app: FastAPI) -> tuple[MetaUnion, ...]:
    """Provides meta items of a response"""
    return (
        MetaCharset(charset="UTF-8"),
        # sane httpquivcontent per https://www.w3schools.com/tags/att_meta_http_equiv.asp
        MetaHTMLEquivContent(
            http_equiv="content-security-policy", content="default-src 'self'"
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


def negotiated(request: Request, resource: APIResource):
    """Returns a negotiated response object"""
    preferred = allowable_content_types(request.headers)[0]
    if preferred == ContentType.JSON:
        # FastAPI itself will render the pydantic object
        # Into a response object
        print(resource.meta)
        return resource
    if preferred == ContentType.HTML:
        # render via the whole HTML rendering machinery
        # which is a whole other module to be designed still
        return HTMLResponse(str(Page(resource)))
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="caannot find acceptable response type for accept header "
        "{request.headers.get('accept')}",
    )
