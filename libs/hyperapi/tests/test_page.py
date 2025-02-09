import factories as f
from hyperapi.components.page import Page
from py_w3c.validators.html.validator import HTMLValidator


def test_page_makes_valid_html():
    resource = Page(resource=f.APIResourceFactory.build(), children=[])
    validator = HTMLValidator()
    validator.validate(str(resource.build()))
    assert not validator.errors, validator.errors
