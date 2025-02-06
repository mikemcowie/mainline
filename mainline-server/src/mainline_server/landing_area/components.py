from dataclasses import dataclass
from textwrap import dedent

from dominate import tags as t  # type: ignore
from hyperapi.components.base import Component
from hyperapi.components.form import Form
from hyperapi.rest_schema import APIResource, BaseResource
from pydantic import Field


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


class GithubRepositoryReference(BaseResource):
    account: str
    name: str


class HomePageEnquiryForm(BaseResource):
    """Schema for homepage form to discover a project's availability"""

    github_repository: GithubRepositoryReference = Field(...)


@dataclass
class HomePage(Component):
    resource: HomePageResource
    children: list[Component]

    def build(self):
        with t.main() as main:
            t.h1(self.resource.object.heading)
            t.br()
            t.p(self.resource.object.detail)
            for link in self.resource.links:
                for action in link.actions:
                    Form.from_json_schema(
                        action.json_schema, action=link.href, method=action.method
                    ).build()
        return main
