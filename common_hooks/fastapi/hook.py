"""Implementation of the fastapi hook using middlewares."""

from typing import Any
from collections.abc import AsyncGenerator, Generator, Callable
from collections.abc import Callable as CallableABC

from fastapi import FastAPI, Request, Response

from common_hooks.conditions.condition import Condition
from common_hooks.core import CoreHook

SyncCallback = Callable[[Request], Generator[None, Response, None] | Generator]
AsyncCallback = Callable[[Request], AsyncGenerator[None, Response] | AsyncGenerator]


class FastAPIHook(CoreHook):
    def attach(
        self,
        callback: SyncCallback | AsyncCallback,
        /,
        *,
        condition: Condition | None = None,
    ) -> None:
        """Attach a sync or async generator-based callback to a condition.

        The callback should accept a `fastapi.Request`, yield once, and after yielding,
        it will receive a `fastapi.Response` object.

        Example (sync):
            def sync_callback(request: Request):
                # Pre-request logic
                ...
                response = yield
                # Post-response logic
                ...

        Example (async):
            async def async_callback(request: Request):
                # Pre-request logic
                ...
                response = yield
                # Post-response logic
                ...
        """
        super().attach(callback, condition=condition)

    def install(self, app: "FastAPI") -> None:
        """Install hooks into the FastAPI application using a middleware."""

        @app.middleware("http")
        async def _fastapi_hook_middleware(request: Request, call_next: CallableABC) -> Any:
            method_type: str = request.method.upper()
            url = str(request.url)

            active_sync_gens: list[Generator[None, Response, None]] = []
            active_async_gens: list[AsyncGenerator[None, Response]] = []

            for callback, condition in self.get_async_hooks():
                if condition is None or condition.matches(url=url, method=method_type):
                    agen = callback(request)
                    await agen.__anext__()
                    active_async_gens.append(agen)

            for callback, condition in self.get_sync_hooks():
                if condition is None or condition.matches(url=url, method=method_type):
                    gen = callback(request)
                    next(gen)
                    active_sync_gens.append(gen)

            response: Response = await call_next(request)

            for agen in active_async_gens:
                try:
                    await agen.asend(response)
                except StopAsyncIteration:
                    pass

            for gen in active_sync_gens:
                try:
                    gen.send(response)
                except StopIteration:
                    pass

            return response


hook = FastAPIHook()
