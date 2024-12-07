"""Test the fastapi hook."""

from fastapi import FastAPI

from common_hooks.fastapi import hook


def callback():
    """A sample callback function."""

    class MyCallbackException(Exception): ...

    raise MyCallbackException("Tes")


hook.attach(callback, mode="before")

app = FastAPI()
hook.apply(app)


@app.get("/test")
def _test_ep():
    """A test route"""
    return "working"
