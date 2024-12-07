"""Definition of a condition to determine when to activate the hook."""

from abc import ABC, abstractmethod


class Condition(ABC):
    """Base class for conditions to create new conditions from."""

    @abstractmethod
    def matches(self, **kwargs) -> bool:
        """Determines if the condition is met based on the provided context.

        Returns:
            bool: True if the condition is met, False otherwise.
        """
