"""Implementation of a exception condition."""

from collections.abc import Container

from .condition import Condition


class ExceptionCondition(Condition):
    """Definition of a http exception condition."""

    def __init__(
        self,
        escaped: bool = False,
        exceptions: Container[Exception] | None = None,
    ) -> None:
        """Initialize the condition.

        Args:
            escaped (bool, optional): Whether to only trigger for non-escaped exceptions
            exceptions (Container[Exception], optional): Exceptions to trigger the condition for
        """
        self.escaped = escaped
        self.exceptions: Container[Exception] = exceptions or set()

    def matches(self, escaped: bool) -> bool:
        """Check if the conditions are met.

        Args:
            escaped (bool): Whether the exception was escaped or not

        Returns:
            bool: True if the condition is met, False otherwise
        """
        return escaped is self.escaped
