"""Implementation of a exception condition."""

from .condition import Condition


class ExceptionCondition(Condition):
    """Definition of a http exception condition."""

    def __init__(
        self,
        escaped: bool = False,
    ) -> None:
        """Initialize the condition.

        Args:
            escaped (bool, optional): Whether to only trigger for non-escaped exceptions
        """
        self.escaped = escaped

    def matches(self, escaped: bool) -> bool:
        """Check if the conditions are met.

        Args:
            escaped (bool): Whether the exception was escaped or not

        Returns:
            bool: True if the condition is met, False otherwise
        """
        return escaped is self.escaped
