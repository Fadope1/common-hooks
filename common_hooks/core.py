"""Implementation of the core hook"""

from inspect import iscoroutinefunction
from typing import Literal
from collections.abc import Callable
from abc import ABC, abstractmethod

from .conditions.condition import Condition


class CoreHook(ABC):
    """CoreHook to inherit from when creating new hooks."""

    def __init__(self) -> None:
        self.pre_hooks: list[tuple[Callable, Condition]] = []
        self.post_hooks: list[tuple[Callable, Condition]] = []
        self._is_async = False

    def attach(
        self,
        callback: Callable,
        *,
        mode: Literal["after"] | Literal["before"] = "after",
        condition: Condition | None = None,
    ) -> None:
        """Attach a callback to a specific condition.

        Args:
            mode (str): When to execute the callback. Must be either 'before' or 'after'.
            callback (callable): The function to be called when the condition is met.
            condition (Condition): An instance of a Condition subclass that must be satisfied to trigger.
        """
        if mode == "after":
            self.post_hooks.append((callback, condition))
        elif mode == "before":
            self.pre_hooks.append((callback, condition))

        if iscoroutinefunction(callback):
            self._is_async = True

        # if condition is None:
        #     condition = Condition() # TODO: Provide always true condition

    @abstractmethod
    def apply(self, *args, **kwargs) -> None:
        """Apply the attached hooks. This method must be overridden by subclasses."""
