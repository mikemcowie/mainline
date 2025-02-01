from typing import Generic, Literal, TypeVar

from pydantic import AliasGenerator, AnyHttpUrl, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake


def to_dash_case(field: str):
    """validation alias generator to convert camel_case to dash-case"""
    return to_snake(field).replace("_", "-")


def from_dash_case(field: str):
    """serialization alias generator to convert camel_case to dash-case"""
    return field


class BaseResource(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=AliasGenerator(
            validation_alias=from_dash_case, serialization_alias=to_dash_case
        ),
    )


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


class BaseMeta(BaseResource):
    """Base classes for the classes that define the <meta> tag
    per https://www.w3schools.com/tags/tag_meta.asp
    """


class MetaCharset(BaseMeta):
    """Defines the data in a <meta charset="UTF-8"> HTML header meta tag
    Per https://www.w3schools.com/tags/att_meta_charset.asp
    """

    charset: str = Field(
        "UTF-8",
        title="charset",
        description=(
            "The charset attribute specifies the character encoding for "
            "the HTML document. The HTML5 specification encourages web "
            "developers to use the UTF-8 character set, which covers "
            "almost all of the characters and symbols in the world!"
        ),
    )


class MetaNameContent(BaseMeta):
    """Defines the data in a <meta name="key" content="value"> HTML tag
    Per https://www.w3schools.com/tags/att_meta_name.asp
    """

    name: str = Field(
        ..., title="name", description="Specifies a name for the metadata"
    )
    content: str = Field(
        ...,
        title="content",
        description=(
            "Specifies the value associated with the http-equiv or name attribute"
        ),
    )


class MetaHTMLEquivContent(BaseMeta):
    """Defines the data in a <meta name="key" content="value"> HTML tag
    Per https://www.w3schools.com/tags/att_meta_name.asp
    """

    http_equiv: Literal[
        "content-security-policy", "content-type", "default-style", "refresh"
    ] = Field(..., title="http equiv", description="Specifies a name for the metadata")
    content: str = Field(
        ...,
        title="content",
        description=(
            "Specifies the value associated with the http-equiv or name attribute"
        ),
    )


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
    meta: tuple[BaseMeta, ...] = Field(
        ..., title="HTML meta attribute", description="HTML meta attributes"
    )
    object: ObjectT = Field(..., alias="object", title="parameterized Object Type")
    links: list[APILink] = Field(..., title="linked resources")
