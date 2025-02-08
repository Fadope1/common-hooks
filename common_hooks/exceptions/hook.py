"""Implementation of the exception hook based on sys.excepthook and sys.settrace

TODO:
- Check if async methods make sense and can work in this case?
- Check if escaped can be extracted from information provided by sys.settrace
"""

import sys
import warnings
from types import TracebackType

from typing import NoReturn, Any
from collections.abc import Generator, Callable
from functools import partial

from common_hooks.conditions import ExceptionCondition
from common_hooks.core import CoreHook

InputParams = tuple[Any, Any, Any, bool]
SyncCallback = Callable[[*InputParams], Generator[None, None, NoReturn] | Generator]


class ExceptionHook(CoreHook):
    def attach(
        self,
        callback: SyncCallback,
        /,
        *,
        condition: ExceptionCondition | None = None,
    ) -> None:
        # todo: add docstring
        super().attach(callback, condition=condition)

    def install(self) -> None:
        """Install hooks into the FastAPI application using a middleware."""

        for callback, condition in self.get_sync_hooks():
            if condition is not None and condition.escaped is False:
                warnings.warn("Catching exceptions add overhead to the application. Use with caution.")
                sys.excepthook = partial(self.handle_excepthook, callback=callback, condition=condition)
            else:  # TODO: fix this
                warnings.warn("Escaped exceptions are extremely impactful on performance. Use with caution.")
                # sys.settrace(partialmethod(self.handle_settrace, callback=callback, condition=condition))

    def handle_excepthook(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        """Handle not escaped errors"""
        if condition.matches(exc_type, False):
            for _ in callback(exc_type, exc_value, exc_traceback, False):
                pass
        else:
            original_hook = sys.excepthook
            sys.excepthook = sys.__excepthook__
            try:
                raise exc_type(exc_value).with_traceback(exc_traceback)
            finally:
                sys.excepthook = original_hook

    def handle_settrace(self, callback, condition: ExceptionCondition, _frame, event, arg):
        """Handle escaped errors"""

        if event == "exception":
            return
            exc_type, exc_value, exc_traceback = arg

            if condition.matches(exc_type, False):
                callback(exc_type, exc_value, exc_traceback, True)  # TODO: calculate the escaped bool


hook = ExceptionHook()
