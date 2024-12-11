"""Implementation of the core hook"""

from __future__ import annotations
import inspect
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING
from collections.abc import Generator, AsyncGenerator, Callable

if TYPE_CHECKING:
    from common_hooks.conditions.condition import Condition


class CoreHook(ABC):
    """CoreHook to store synchronous and asynchronous generator callbacks."""

    def __init__(self) -> None:
        self._sync_hooks: list[tuple[Callable[..., Generator[Any, Any, Any]], Condition | None]] = []
        self._async_hooks: list[tuple[Callable[..., AsyncGenerator[Any, Any]], Condition | None]] = []

    def attach(
        self,
        callback: Callable[..., Any],
        /,
        *,
        condition: Condition | None = None,
    ) -> None:
        """Attach a generator-based callback to a condition.

        Raises:
            TypeError: If callback is not a generator or async generator function.
        """
        if inspect.isasyncgenfunction(callback):
            self._async_hooks.append((callback, condition))
        elif inspect.isgeneratorfunction(callback):
            self._sync_hooks.append((callback, condition))
        else:
            raise TypeError(
                "callback must be a generator function or an async generator function (must contain a yield)."
            )

    def get_sync_hooks(self):
        return self._sync_hooks

    def get_async_hooks(self):
        return self._async_hooks

    @abstractmethod
    def install(self, *args, **kwargs) -> None:
        """Install the attached hooks. Must be overridden by subclasses."""

    # TODO: Implement uninstall method
    # @abstractmethod
    # def uninstall(self, *args, **kwargs) -> None:
    #     """Uninstall the attached hooks. Must be overridden by subclasses."""
