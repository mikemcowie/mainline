from hyperapi.components.head import (
    APIResource,
    RemoteScript,
    RemoteStyleSheet,
)
from hyperapi.rest_schema import (
    MetaCharset,
    MetaHTMLEquivContent,
    MetaNameContent,
)
from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory


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
