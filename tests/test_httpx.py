import pytest
from collections.abc import Generator

import httpx
from common_hooks.conditions import HttpCondition
from common_hooks.httpx import hook

from .exceptions import PreCallbackError, PostCallbackError

URL = "https://test.com"


def sync_callback_pre(request: httpx.Request) -> Generator:
    raise PreCallbackError("Pre-request code called")
    _ = yield


def sync_callback_post(request: httpx.Request) -> Generator:
    _ = yield
    raise PostCallbackError("Post-response code called")


def test_sync_callback_pre_exception(httpx_mock):
    httpx_mock.add_response(url=URL, status_code=200, json={"message": "ok"})

    condition = HttpCondition(methods=["GET"])
    hook.attach(sync_callback_pre, condition=condition)
    hook.install()

    with pytest.raises(PreCallbackError) as exc_info:
        with httpx.Client() as client:
            client.get(URL)


def test_sync_callback_post_exception(httpx_mock):
    httpx_mock.add_response(url=URL, status_code=200, json={"message": "ok"})

    condition = HttpCondition(methods=["GET"])
    hook.attach(sync_callback_post, condition=condition)
    hook.install()

    with pytest.raises(PostCallbackError) as exc_info:
        with httpx.Client() as client:
            client.get(URL)
