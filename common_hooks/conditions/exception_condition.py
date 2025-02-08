"""Implementation of a exception condition.

Todos:
- Exception list cannot be empty. Empty should mean all is accepted.

Ideas:
- split exceptions into two categories. Type check and subclass check?
"""

from collections.abc import Container

from .condition import Condition


class ExceptionCondition(Condition):
    """Definition of a http exception condition."""

    def __init__(
        self,
        escaped: bool = False,
        exceptions: Container[type[Exception]] | None = None,
    ) -> None:
        """Initialize the condition.

        Args:
            escaped (bool, optional): Whether to only trigger for non-escaped exceptions
            exceptions (Container[type[Exception]], optional): Exceptions to trigger the condition for (empty means all).
        """
        self.escaped = escaped
        self.exceptions: Container[type[Exception]] = exceptions or set()

    def matches(self, exception: type[BaseException], escaped: bool) -> bool:
        """Check if the conditions are met.

        Args:
            exception (Exception): The exception that occured
            escaped (bool): Whether the exception was escaped

        Returns:
            bool: True if the condition is met, False otherwise
        """
        return all({exception in self.exceptions, escaped is self.escaped})
