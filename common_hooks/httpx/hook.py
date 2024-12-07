"""Implementation of the httpx hook using event hooks."""

import httpx

from common_hooks.core import CoreHook


class HttpxHook(CoreHook):
    """Hook to attach to the httpx package."""

    def apply(self) -> None:
        """Apply the attached hooks to the httpx client by using event hooks."""
        # Save the original __init__ methods
        original_async_client_init = httpx.AsyncClient.__init__
        original_client_init = httpx.Client.__init__

        # Define custom __init__ methods that add our event hooks
        def custom_async_client_init(this, *args, **kwargs):
            if "event_hooks" not in kwargs:
                kwargs["event_hooks"] = {"request": [], "response": []}
            else:
                if "request" not in kwargs["event_hooks"]:
                    kwargs["event_hooks"]["request"] = []
                if "response" not in kwargs["event_hooks"]:
                    kwargs["event_hooks"]["response"] = []

            # Add our hooks
            kwargs["event_hooks"]["request"].append(self._async_request_event_hook)
            kwargs["event_hooks"]["response"].append(self._async_response_event_hook)

            original_async_client_init(this, *args, **kwargs)

        # Replace the __init__ method
        httpx.AsyncClient.__init__ = custom_async_client_init  # type: ignore

        def custom_client_init(this, *args, **kwargs):
            if "event_hooks" not in kwargs:
                kwargs["event_hooks"] = {"request": [], "response": []}
            else:
                if "request" not in kwargs["event_hooks"]:
                    kwargs["event_hooks"]["request"] = []
                if "response" not in kwargs["event_hooks"]:
                    kwargs["event_hooks"]["response"] = []

            # Add our hooks
            kwargs["event_hooks"]["request"].append(self._sync_request_event_hook)
            kwargs["event_hooks"]["response"].append(self._sync_response_event_hook)

            original_client_init(this, *args, **kwargs)

        # Replace the __init__ method
        httpx.Client.__init__ = custom_client_init  # type: ignore

    async def _async_request_event_hook(self, request: httpx.Request):
        method = request.method
        url = str(request.url)
        for callback, condition in self.pre_hooks:
            if condition.matches(url=url, method=method):
                if self._is_async:
                    await callback(request)
                else:
                    callback(request)

    async def _async_response_event_hook(self, response: httpx.Response):
        method = response.request.method
        url = str(response.request.url)
        for callback, condition in self.post_hooks:
            if condition.matches(url=url, method=method):
                if self._is_async:
                    await callback(response)
                else:
                    callback(response)

    def _sync_request_event_hook(self, request: httpx.Request):
        method = request.method
        url = str(request.url)
        for callback, condition in self.pre_hooks:
            if condition.matches(url=url, method=method):
                callback(request)

    def _sync_response_event_hook(self, response: httpx.Response):
        method = response.request.method
        url = str(response.request.url)
        for callback, condition in self.post_hooks:
            if condition.matches(url=url, method=method):
                callback(response)


# Instantiate the hook
hook = HttpxHook()
