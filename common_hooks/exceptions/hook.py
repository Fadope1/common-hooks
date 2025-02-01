"""Implementation of the exception hook based on sys.excepthook and sys.settrace

TODO:
- Check if async methods make sense and can work in this case?
- Check if escaped can be extracted from information provided by sys.settrace
"""

import sys

from typing import NoReturn, Any
from collections.abc import AsyncGenerator, Generator, Callable
from functools import partial

from common_hooks.conditions import ExceptionCondition
from common_hooks.core import CoreHook

InputParams = tuple[Any, Any, Any, bool]
SyncCallback = Callable[[*InputParams], Generator[None, None, NoReturn] | Generator]
AsyncCallback = Callable[[*InputParams], AsyncGenerator[None, NoReturn] | AsyncGenerator]


class ExceptionHook(CoreHook):
    def attach(
        self,
        callback: SyncCallback | AsyncCallback,
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
                sys.excepthook = partial(self.handle_simple_exception, callback=callback, condition=condition)
            # else: # TODO: fix this
            #     sys.settrace(partialmethod(self.handle_advanced_exception, callback=callback, condition=condition))

    def handle_simple_exception(self, exc_type, exc_value, exc_traceback, callback, condition: ExceptionCondition):
        """Handle not escaped errors"""
        print("checking condition")

        if condition.matches(exc_type, False):
            for _ in callback():
                pass
        else:
            raise  #! this causes "RuntimeError: No active exception to reraise" - rebuilt exception?

    def handle_advanced_exception(self, callback, condition: ExceptionCondition, _frame, event, arg):
        """Handle escaped errors"""

        if event == "exception":
            exc_type, exc_value, exc_traceback = arg

            if condition.matches(exc_type, False):
                callback(exc_type, exc_value, exc_traceback, True)  # TODO: calculate the escaped bool


hook = ExceptionHook()
