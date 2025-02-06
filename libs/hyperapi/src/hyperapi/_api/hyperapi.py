from datetime import datetime
from fastapi import FastAPI, APIRouter as _APIRouter
from dataclasses import dataclass
from functools import cached_property
from typing import NamedTuple, Callable, TYPE_CHECKING, Any, Collection
from collections import OrderedDict
import structlog
from fastapi.routing import APIRoute
from pydantic import BaseModel
from http import HTTPMethod

try:
    import structlog

    logger = structlog.get_logger()
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


class Endpoint(NamedTuple):
    path: str
    method: HTTPMethod


@dataclass
class Route:
    func: Callable

    @cached_property
    def input_model(self) -> type[BaseModel] | None:
        """Looks up the endpoint function's type
        annotations to work out whether it has an
        input model
        """
        for v in self.func.__annotations__.values():
            try:
                if issubclass(v, BaseModel):
                    # Unannotated
                    return v
            except TypeError:
                pass
            # Annotated (or anything that ducktypes like it)
            try:
                if issubclass(v.__origin__, BaseModel):
                    return v.__origin__
            except (AttributeError, TypeError):
                pass
        return None


REGISTRY: dict[FastAPI, dict[Endpoint, Route]] = {}


def register_routes(app: FastAPI):
    if app not in REGISTRY.keys():
        logger.info(f"adding {app=} to registry")
        REGISTRY[app] = {}
    for api_route in app.routes:
        if isinstance(api_route, APIRoute):
            for method in api_route.methods:
                route = Route(
                    app=app, route=api_route, method=method, func=api_route.endpoint
                )
                endpoint = Endpoint(path=api_route.path, method=method)
                logger.info(
                    f"adding {endpoint=}:{route=} to registry, with model={route.input_model}"
                )
                REGISTRY[app][endpoint] = route


class APIRouter(_APIRouter):
    registry: OrderedDict[Endpoint, Route]

    if not TYPE_CHECKING:
        # Don't let the type checker see the updated methods
        # The use of *args/**kwargs would worsen the completions
        # that the IDE can use compared to using FastAPI
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.registry = OrderedDict()

        def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs):
            super().add_api_route(path, endpoint, **kwargs)
            methods = kwargs["methods"]
            if isinstance(methods, Collection):
                for method in methods:
                    endpoint = Endpoint(path=path, method=method)
                    route = Route(func=endpoint)
                    logger.debug(f"registering {endpoint=} {route=} on router {self}")
                    self.registry[endpoint] = route


class HyperAPI(FastAPI):
    """FastAPI subclass with helpers for building hypermedia APIs"""

    registry: OrderedDict[Endpoint, Route]
    created: datetime

    if not TYPE_CHECKING:
        # Don't let the type checker see the updated methods
        # The use of *args/**kwargs would worsen the completions
        # that the IDE can use compared to using FastAPI
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.registry = OrderedDict()
            self.created = datetime.now()

        def include_router(self, router: APIRouter, **kwargs):
            super().include_router(router, **kwargs)
            for endpoint, route in router.registry.items():
                logger.info(f"including {endpoint=} {route=} in app={self}")
                self.registry[endpoint] = route

    def __repr__(self):
        return f"{self.__class__.__name__}/title={self.title}/created={self.created})"
