"""Class to handle asyncio exceptions"""

import asyncio
from types import TracebackType

from common_hooks.conditions import ExceptionCondition
from ..exception_types import CallbackTypes


class AsyncioExcepthookHandler:
    def install_excepthook(
        self,
        callback: CallbackTypes,
        condition: ExceptionCondition,
    ) -> None:
        loop = asyncio.get_event_loop()

        def handle_asyncio_excepthook(loop: asyncio.AbstractEventLoop, context: dict) -> None:
            exc = context.get("exception")
            if exc is None:
                message = context.get("message", "Unknown error")
                exc = Exception(message)
            exc_type = type(exc)
            exc_value = exc
            exc_traceback = exc.__traceback__
            self.handle_exception(exc_type, exc_value, exc_traceback, callback=callback, condition=condition)

        loop.set_exception_handler(handle_asyncio_excepthook)

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
        *,
        callback: CallbackTypes,
        condition: ExceptionCondition,
    ) -> None:
        if condition.matches(exc_type, False):
            for _ in callback(exc_type, exc_value, exc_traceback, False):
                pass
        else:
            loop = asyncio.get_event_loop()
            context = {
                "exception": exc_value,
                "message": str(exc_value),
                "exc_type": exc_type,
                "exc_traceback": exc_traceback,
            }
            loop.default_exception_handler(context)
