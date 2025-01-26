from collections.abc import Generator
import pytest

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from common_hooks.fastapi import hook
from common_hooks.conditions import HttpCondition

from .exceptions import PreCallbackError, PostCallbackError


def sync_callback_pre(request: Request) -> Generator:
    raise PreCallbackError("Pre-request code called")
    _ = yield


def sync_callback_post(request: Request) -> Generator:
    _ = yield
    raise PostCallbackError("Post-response code called")


@pytest.fixture
def app():
    app = FastAPI()

    @app.get("/test")
    def read_test():
        return {"hello": "world"}

    return app


def test_fastapi_sync_callback_pre_exception(app):
    condition = HttpCondition(methods=["GET"])
    hook.attach(sync_callback_pre, condition=condition)
    hook.install(app)

    client = TestClient(app)
    with pytest.raises(PreCallbackError) as exc_info:
        client.get("/test")


def test_fastapi_sync_callback_post_exception(app):
    condition = HttpCondition(methods=["GET"])
    hook.attach(sync_callback_post, condition=condition)
    hook.install(app)

    client = TestClient(app)
    with pytest.raises(PostCallbackError) as exc_info:
        client.get("/test")
