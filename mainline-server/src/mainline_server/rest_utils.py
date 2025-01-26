from enum import StrEnum
from typing import Mapping

from fastapi import HTTPException, Request, status

from mainline_server.rest_schema import APILink


class ContentType(StrEnum):
    JSON = "application/json"
    HTML = "text/html"
    PLAINTEXT = "text/plain"


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
