from py_w3c.validators.html.validator import HTMLValidator

from mainline_server.ui.page import Page
from tests import factories as f


def test_page_makes_valid_html():
    resource = Page(resource=f.APIResourceFactory.build())
    validator = HTMLValidator()
    validator.validate(str(resource.build()))
    assert not validator.errors, validator.errors
