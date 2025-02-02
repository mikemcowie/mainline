from dataclasses import dataclass
from textwrap import dedent

from dominate import tags as t  # type: ignore
from pydantic import Field

from mainline_server.rest_schema import APIResource, BaseResource
from mainline_server.ui.components.base import Component


class HomePageCopy(BaseResource):
    heading: str = Field(..., title="Page heading")
    detail: str = Field(..., title="Page deatail")


class COPY:
    """Data holder for the homepage content"""

    HEADING = "Take your python project live in minutes by taking the mainline"
    DETAIL = dedent(
        """
        Bring your idea to life without compromising on security and uptime.

        Simply add a couple of lines to your pyproject.toml, and we'll build, test, and
        deploy it with production-grade CI/CD pipelines.

        Enter your project details to get started
        """
    )


HomePageResource = APIResource[HomePageCopy]


@dataclass
class HomePage(Component):
    resource: HomePageResource
    children: list[Component]

    def build(self):
        with t.main() as main:
            t.h1(self.resource.object.heading)
            t.br()
            t.p(self.resource.object.detail)
        return main
