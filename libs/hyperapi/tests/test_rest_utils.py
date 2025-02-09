import pytest
from fastapi import HTTPException
from hyperapi import rest_utils

WEB_BROWSER_ACCEPTS_HEADER = (
    "Accept: text/html, application/xhtml+xml, "
    "application/xml;q=0.9, image/webp, */*;q=0.8"
)
REQUEST_ACCEPTS_HEADER = "*/*"
JSON_ACCEPTS_HEADER = "application/json"
TEXT_ACCEPTS_HEADER = "text/plain"


def test_web_browser_returns_html_resopnse_preferred():
    assert rest_utils.allowable_content_types(
        headers={"accept": WEB_BROWSER_ACCEPTS_HEADER}
    ) == [rest_utils.ContentType.HTML]


def test_wildcard_accepts_returns_json_respnse_preferred():
    assert rest_utils.allowable_content_types(
        headers={"accept": REQUEST_ACCEPTS_HEADER}
    ) == [
        rest_utils.ContentType.JSON,
        rest_utils.ContentType.HTML,
        rest_utils.ContentType.PLAINTEXT,
    ]


def test_json_accepts_returns_json_respnse_preferred():
    assert rest_utils.allowable_content_types(
        headers={"accept": JSON_ACCEPTS_HEADER}
    ) == [rest_utils.ContentType.JSON]


def test_plaintext_accepts():
    assert rest_utils.allowable_content_types(
        headers={"accept": TEXT_ACCEPTS_HEADER}
    ) == [rest_utils.ContentType.PLAINTEXT]


def test_unacceptable():
    with pytest.raises(HTTPException):
        rest_utils.allowable_content_types(headers={"accept": "application/yaml"})
