"""Implementation of the exception hook based on sys.excepthook and sys.settrace"""

from collections.abc import AsyncGenerator, Generator, Callable


from common_hooks.conditions.condition import Condition
from common_hooks.core import CoreHook

SyncCallback = Callable[[None], Generator[None, None, None] | Generator]
AsyncCallback = Callable[[None], AsyncGenerator[None, None] | AsyncGenerator]


class ExceptionHook(CoreHook):
    def attach(
        self,
        callback: SyncCallback | AsyncCallback,
        /,
        *,
        condition: Condition | None = None,
    ) -> None:
        super().attach(callback, condition=condition)

    def install(self) -> None:
        """Install hooks into the FastAPI application using a middleware."""
        pass


hook = ExceptionHook()
