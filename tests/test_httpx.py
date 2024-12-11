"""Test the httpx hook."""

import httpx

from common_hooks.conditions import HttpRequestCondition

from common_hooks.httpx import hook as test  # works


async def callback():
    """A sample callback function."""

    class MyCallbackException(Exception): ...

    raise MyCallbackException("Tes")


complex_condition = HttpRequestCondition(methods=["GET", "POST"])
hook.attach(callback, mode="after", condition=complex_condition)

# hook.attach(callback).when("after").methods(["GET", "POST"]).url_pattern("/v1") # alternative POC

hook.install()

with httpx.Client(url="127.0.0.1") as client:
    client.get("/test")
