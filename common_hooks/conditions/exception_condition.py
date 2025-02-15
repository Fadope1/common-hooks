"""Implementation of a exception condition.

Todos:
- Exception list cannot be empty. Empty should mean all is accepted.

Ideas:
- split exceptions into two categories. Type check and subclass check?
"""

from collections.abc import Collection

from .condition import Condition


class ExceptionCondition(Condition):
    """Definition of a http exception condition."""

    def __init__(
        self,
        escaped: bool = False,
        exceptions: Collection[type[Exception]] | None = None,
        check_subclass: bool = False,
    ) -> None:
        """Initialize the condition.

        Args:
            escaped (bool, optional): Whether to only trigger for non-escaped exceptions
            exceptions (Collection[type[Exception]], optional): Exceptions to trigger the condition for (empty means all).
            check_subclass (bool, optional): Whether to check if the exception is a subclass of any in exceptions or exact match.
        """
        self.escaped = escaped
        self.exceptions: Collection[type[Exception]] = exceptions or set()
        self.check_subclass = check_subclass

    def matches(self, exception: type[BaseException], escaped: bool) -> bool:
        """Check if the conditions are met.

        Args:
            exception (Exception): The exception that occurred
            escaped (bool): Whether the exception was escaped

        Returns:
            bool: True if the condition is met, False otherwise
        """
        if self.check_subclass:
            exception_match = any(issubclass(exception, exc) for exc in self.exceptions)
        else:
            exception_match = exception in self.exceptions
        return all({exception_match, escaped is self.escaped})
