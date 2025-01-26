from typing import Generic, TypeVar

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class BaseResource(BaseModel):
    model_config = ConfigDict(extra="forbid")


class APILink(BaseResource):
    href: AnyHttpUrl = Field(
        ...,
        title="Link destination",
        description=(
            "Hypermedia link to a resource. The basis of hyperlinks in the web browser"
        ),
    )
    name: str = Field(
        ...,
        title="Link Name",
        description=(
            "Identifier of a link. "
            "Typically used in the UI as the displayed text of a link or button"
        ),
    )


ObjectT = TypeVar("ObjectT")


class APIResource(BaseResource, Generic[ObjectT]):
    """The base resource for all response objects"""

    self: APILink = Field(
        ..., title="Current", description="Link to the current resource represented"
    )
    title: str = Field(
        ...,
        title="Title",
        description=(
            "The title of the resource. "
            "Used to render into the HTML page title for HTML resources."
        ),
    )
    object: ObjectT = Field(..., alias="object", title="parameterized Object Type")
    links: list[APILink] = Field(..., title="linked resources")
