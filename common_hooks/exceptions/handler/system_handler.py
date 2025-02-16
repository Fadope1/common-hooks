"""Class to handle the normal sync system exception"""

import sys
from types import TracebackType
from functools import partial

from common_hooks.conditions import ExceptionCondition
from common_hooks.exceptions.exception_types import CallbackTypes, SyncCallback


class SysExcepthookHandler:
    def install_excepthook(
        self,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        sys.excepthook = partial(self.handle_exception, callback=callback, condition=condition)

    def handle_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
        *,
        callback: SyncCallback,
        condition: ExceptionCondition,
    ) -> None:
        if condition.matches(exc_type, False):
            for _ in callback(exc_type, exc_value, exc_traceback, False):
                pass
        else:
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
