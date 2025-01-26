from collections.abc import Generator
import pytest

from common_hooks.exceptions import hook
from common_hooks.conditions import ExceptionCondition


def callback():
    print("callback called")


def handled_exception() -> Generator:
    try:
        raise ValueError("Pre-request code called")
    except ValueError:
        pass


def unhandled_exception() -> Generator:
    raise ValueError("Post-response code called")


def test_unhandled_exception():
    condition = ExceptionCondition()
    hook.attach(callback, condition=condition)
    hook.install()
    
    unhandled_exception()

