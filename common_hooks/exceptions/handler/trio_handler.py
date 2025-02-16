"""Class to handle Trio exceptions"""

from types import TracebackType

try:
    import trio
except ImportError:
    trio = None

from common_hooks.conditions import ExceptionCondition
from ..exception_types import CallbackTypes


class TrioExcepthookHandler:
    def install_excepthook(
        self,
        callback: CallbackTypes,
        condition: ExceptionCondition,
    ) -> None:
        if trio is None:
            return None

        async def trio_handle_exception(
            exc_type: type[BaseException],
            exc_value: BaseException,
            exc_traceback: TracebackType,
        ) -> None:
            if condition.matches(exc_type, False):
                for _ in callback(exc_type, exc_value, exc_traceback, False):
                    pass
            else:
                trio.lowlevel._run_trio_excepthook(exc_type, exc_value, exc_traceback)

        trio.hazmat.install_global_exception_handler(trio_handle_exception)
