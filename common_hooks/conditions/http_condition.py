"""Implementation of a http request condition."""

from collections.abc import Collection
from typing import Literal

from .condition import Condition

Methods = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD", "CONNECT", "TRACE"]


class HttpCondition(Condition):
    """Definition of a http request condition."""

    def __init__(self, methods: Collection[Methods] | None = None):
        """TODO:
        url_pattern? -> regex pattern
        urls? -> list of urls
        """
        self.methods: Collection[Methods] = methods or set()

    def matches(self, method: Methods, url: str) -> bool:
        """Check if the conditions are met."""
        return all({method.upper() in self.methods, len(self.methods) != 0})
