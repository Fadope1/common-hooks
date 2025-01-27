"""Tests for the exception hook"""

import pytest

from common_hooks.exceptions import hook
from common_hooks.conditions import ExceptionCondition

from .exceptions import PreCallbackError, PostCallbackError


def sync_callback_pre(exception: Exception, escaped: bool):
    """callback for testing pre hook"""
    raise PreCallbackError("Pre-request code called")
    yield


def sync_callback_post(exception: Exception, escaped: bool):
    """callback for checking post hook"""
    yield
    raise PostCallbackError("Pre-request code called")


def handled_exception():
    try:
        raise ValueError("Pre-request code called")
    except ValueError:
        pass


def unhandled_exception():
    raise ValueError()


def test_unhandled_exception():
    condition = ExceptionCondition()
    hook.attach(sync_callback_pre, condition=condition)
    hook.install()

    with pytest.raises(PreCallbackError):
        unhandled_exception()

    handled_exception()  # should not raise any exceptions/ call a hook

    # test the post hook
    # hook.uninstall()
    # hook.attach(sync_callback_post, condition=condition)

    # with pytest.raises(PostCallbackError):
    #     unhandled_exception()


def test_handled_exception():
    condition = ExceptionCondition(escaped=True)
    hook.attach(sync_callback_pre, condition=condition)
    hook.install()

    with pytest.raises(PreCallbackError):
        handled_exception()

    # test the post hook
    # hook.uninstall()
    # hook.attach(sync_callback_post, condition=condition)

    # with pytest.raises(PostCallbackError):
    #     handled_exception()


def test_specific_exception():
    condition = ExceptionCondition(exceptions={SyntaxError})
    hook.attach(sync_callback_pre, condition=condition)
    hook.install()

    with pytest.raises(ValueError):
        unhandled_exception()
