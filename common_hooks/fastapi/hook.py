"""Implemenation of the fastapi hook using middlewares."""

from typing import TYPE_CHECKING, Any
from collections.abc import Callable

if TYPE_CHECKING:
    from fastapi import FastAPI, Request

from common_hooks.core import CoreHook


class FastAPIHook(CoreHook):
    def apply(self, app: "FastAPI") -> None:
        """Apply the attached hooks to the FastAPI app by using middlewares."""

        @app.middleware("http")
        async def _fastapi_hook_middleware(request: "Request", call_next: Callable) -> Any:
            method_type: str = request.method.upper()
            url = str(request.url)

            # Execute 'before' hooks
            for callback, condition in self.pre_hooks:
                if condition.matches(url=url, method=method_type):
                    if self._is_async:
                        await callback()
                    else:
                        callback()

            response = await call_next(request)

            # Execute 'after' hooks
            for callback, condition in self.post_hooks:
                if condition.matches(url=url, method=method_type):
                    if self._is_async:
                        await callback()
                    else:
                        callback()

            return response


hook = FastAPIHook()
