"""Implementation of the exception hook based on sys.excepthook and sys.settrace

TODO:
- Check if async methods make sense and can work in this case?
- Check if escaped can be extracted from information provided by sys.settrace
"""

from typing import Protocol
import sys
import warnings
from types import TracebackType

from common_hooks.exceptions.exception_types import CallbackTypes, SyncCallback
from .handler import (
    SysExcepthookHandler,
    # ThreadingExcepthookHandler,
    # AsyncioExcepthookHandler,
    # TrioExcepthookHandler,
)
from common_hooks.conditions import ExceptionCondition
from common_hooks.core import CoreHook


class ExceptionHandler(Protocol):
    def install_excepthook(
        self,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        """Tries to install the exception handler with the given callback and condition."""
        ...

    # def install_trace()


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

    def install(
        self,
        handlers: list[ExceptionHandler] | None = None,
    ) -> None:
        """Install hooks into the application, supporting both synchronous and asynchronous exceptions."""

        if handlers is None:
            handlers = [
                SysExcepthookHandler(),  # type: ignore # For some reason pylance cannot understand the type
                # ThreadingExcepthookHandler(),
                # AsyncioExcepthookHandler(),
                # TrioExcepthookHandler(),
            ]

        for callback, condition in self.get_sync_hooks():
            if condition is not None and condition.escaped is False:
                warnings.warn("Catching exceptions adds overhead to the application. Use with caution.")
                if condition is None or not condition.escaped:
                    for handler in handlers:  # type: ignore # For some reason pylance cannot understand the type
                        handler.install_excepthook(callback, condition)
                # self.install_except_hooks(callback, condition)
            else:
                warnings.warn("Escaped exceptions are extremely impactful on performance. Use with caution.")
                # sys.settrace(partialmethod(self.handle_settrace, callback=callback, condition=condition)) #! will implement this later

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
