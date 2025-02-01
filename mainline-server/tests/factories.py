from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory

from mainline_server.rest_schema import (
    MetaCharset,
    MetaHTMLEquivContent,
    MetaNameContent,
)
from mainline_server.ui.components.head import (
    APIResource,
    RemoteScript,
    RemoteStyleSheet,
)


class APIResourceFactory(ModelFactory[APIResource]):
    pass


class RemoteStyleSheetFactory(DataclassFactory[RemoteStyleSheet]):
    pass


class RemoteScriptFactory(DataclassFactory[RemoteScript]):
    pass


class MetaCharsetFactory(ModelFactory[MetaCharset]):
    pass


class MetaHTMLEquivContentFactory(ModelFactory[MetaHTMLEquivContent]):
    pass


class MetaNameContentFactory(ModelFactory[MetaNameContent]):
    pass
