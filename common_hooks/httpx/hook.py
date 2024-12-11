"""Implementation of the httpx hook using event hooks."""

import httpx
from typing import Any
from collections.abc import Generator, AsyncGenerator, Callable

from common_hooks.core import CoreHook
from common_hooks.conditions.condition import Condition

SyncCallback = Callable[[httpx.Request], Generator[None, httpx.Response, None] | Generator]
AsyncCallback = Callable[[httpx.Request], AsyncGenerator[None, httpx.Response] | AsyncGenerator]


class HttpxHook(CoreHook):
    """Hook to attach to the httpx package with generator-based callbacks."""

    def __init__(self) -> None:
        super().__init__()
        self._active_sync_callbacks: dict[int, list[Generator[Any, Any, Any]] | Any] = {}
        self._active_async_callbacks: dict[int, list[AsyncGenerator[Any, Any]]] = {}

    def attach(
        self,
        callback: SyncCallback | AsyncCallback,
        /,
        *,
        condition: Condition | None = None,
    ) -> None:
        """Attach a sync or async generator-based callback to a condition.

        The callback should:
        - Accept an `httpx.Request` as an argument.
        - Yield exactly once. The code before `yield` executes before the request.
        - After the request completes, a `httpx.Response` object is sent into the generator
          to run post-request logic.

        Example (sync):
            def sync_callback(request: httpx.Request):
                # Pre-request logic
                ...
                response = yield
                # Post-response logic
                ...

        Example (async):
            async def async_callback(request: httpx.Request):
                # Pre-request logic
                ...
                response = yield
                # Post-response logic
                ...
        """
        super().attach(callback, condition=condition)

    def install(self) -> None:
        """Install the attached hooks into httpx.Client and httpx.AsyncClient."""

        original_async_client_init = httpx.AsyncClient.__init__
        original_client_init = httpx.Client.__init__

        def custom_async_client_init(this, *args, **kwargs):
            if "event_hooks" not in kwargs:
                kwargs["event_hooks"] = {"request": [], "response": []}
            else:
                kwargs["event_hooks"].setdefault("request", [])
                kwargs["event_hooks"].setdefault("response", [])

            kwargs["event_hooks"]["request"].append(self._async_request_event_hook)
            kwargs["event_hooks"]["response"].append(self._async_response_event_hook)

            original_async_client_init(this, *args, **kwargs)

        httpx.AsyncClient.__init__ = custom_async_client_init  # type: ignore

        def custom_client_init(this, *args, **kwargs):
            if "event_hooks" not in kwargs:
                kwargs["event_hooks"] = {"request": [], "response": []}
            else:
                kwargs["event_hooks"].setdefault("request", [])
                kwargs["event_hooks"].setdefault("response", [])

            kwargs["event_hooks"]["request"].append(self._sync_request_event_hook)
            kwargs["event_hooks"]["response"].append(self._sync_response_event_hook)

            original_client_init(this, *args, **kwargs)

        httpx.Client.__init__ = custom_client_init  # type: ignore

    # Async event hooks
    async def _async_request_event_hook(self, request: httpx.Request):
        request_id = id(request)
        active_async_gens = []
        method = request.method
        url = str(request.url)

        for callback, condition in self.get_async_hooks():
            if condition is None or condition.matches(url=url, method=method):
                agen = callback(request)
                await agen.asend(None)  # Advance to the yield
                active_async_gens.append(agen)

        if active_async_gens:
            self._active_async_callbacks[request_id] = active_async_gens

    async def _async_response_event_hook(self, response: httpx.Response):
        request = response.request
        request_id = id(request)
        async_gens = self._active_async_callbacks.pop(request_id, [])

        for agen in async_gens:
            try:
                await agen.asend(response)
            except StopAsyncIteration:
                pass

    # Sync event hooks
    def _sync_request_event_hook(self, request: httpx.Request):
        request_id = id(request)
        active_gens = []
        method = request.method
        url = str(request.url)

        for callback, condition in self.get_sync_hooks():
            if condition is None or condition.matches(url=url, method=method):
                gen = callback(request)
                next(gen)  # Advance to the yield
                active_gens.append(gen)

        if active_gens:
            self._active_sync_callbacks[request_id] = active_gens

    def _sync_response_event_hook(self, response: httpx.Response):
        request = response.request
        request_id = id(request)
        gens = self._active_sync_callbacks.pop(request_id, [])

        for gen in gens:
            try:
                gen.send(response)
            except StopIteration:
                pass


hook = HttpxHook()
