from collections.abc import Generator
import pytest

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from common_hooks.fastapi import hook
from common_hooks.conditions import HttpRequestCondition

from .exceptions import PreRequestCallbackError, PostRequestCallbackError


def sync_callback_pre(request: Request) -> Generator:
    raise PreRequestCallbackError("Pre-request code called")
    _ = yield


def sync_callback_post(request: Request) -> Generator:
    _ = yield
    raise PostRequestCallbackError("Post-response code called")


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/test")
    def read_test():
        return {"hello": "world"}

    return app


def test_fastapi_sync_callback_pre_exception(app):
    condition = HttpRequestCondition(methods=["GET"])
    hook.attach(sync_callback_pre, condition=condition)
    hook.install(app)

    client = TestClient(app)
    with pytest.raises(PreRequestCallbackError) as exc_info:
        client.get("/test")


def test_fastapi_sync_callback_post_exception(app):
    condition = HttpRequestCondition(methods=["GET"])
    hook.attach(sync_callback_post, condition=condition)
    hook.install(app)

    client = TestClient(app)
    with pytest.raises(PostRequestCallbackError) as exc_info:
        client.get("/test")
