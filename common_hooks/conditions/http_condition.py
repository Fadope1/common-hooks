"""Implementation of a http request condition."""

from collections.abc import Iterable

from .condition import Condition


class HttpRequestCondition(Condition):
    """Definition of a http request condition."""

    def __init__(self, methods: Iterable | None = None):
        """TODO:
        url_pattern? -> regex pattern
        urls? -> list of urls
        """
        self.methods = methods

    def matches(self, method: str, url: str) -> bool:
        """Check if the condition is met."""
        return any([method.upper() in self.methods, not self.methods])

        # if self.method and self.method != method.upper():
        #     return False
        return True
