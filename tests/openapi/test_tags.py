from typing import Any, Type

import pytest
from openapi_schema_pydantic import OpenAPI

from starlite import Controller, HTTPRouteHandler, Router, Starlite, get


@pytest.fixture
def handler() -> HTTPRouteHandler:
    @get("/handler", tags=["handler"])
    def _handler() -> Any:
        ...

    return _handler


@pytest.fixture
def controller() -> Type[Controller]:
    class _Controller(Controller):
        path = "/controller"
        tags = ["controller"]

        @get(tags=["handler"])
        def _handler(self) -> Any:
            ...

    return _Controller


@pytest.fixture
def router(controller: Type[Controller]) -> Router:
    return Router(path="/router", route_handlers=[controller], tags=["router"])


@pytest.fixture
def app(handler: HTTPRouteHandler, controller: Type[Controller], router: Router) -> Starlite:
    return Starlite(route_handlers=[handler, controller, router])


@pytest.fixture
def openapi_schema(app: Starlite) -> OpenAPI:
    return app.openapi_schema


def test_openapi_schema_handler_tags(openapi_schema: OpenAPI) -> None:
    assert openapi_schema.paths["/handler"].get.tags == ["handler"]


def test_openapi_schema_controller_tags(openapi_schema: OpenAPI) -> None:
    assert set(openapi_schema.paths["/controller"].get.tags) == {"handler", "controller"}


def test_openapi_schema_router_tags(openapi_schema: OpenAPI) -> None:
    assert set(openapi_schema.paths["/router/controller"].get.tags) == {"handler", "controller", "router"}
