"""Types for different signatures"""

from typing import Any, NoReturn, TypeVar
from collections.abc import Callable, Generator

InputParams = tuple[Any, Any, Any, bool]
SyncCallback = Callable[[*InputParams], Generator[None, None, NoReturn | None]]
AsyncCallback = Callable[[*InputParams], Generator[None, None, NoReturn | None]]

CallbackTypes = TypeVar("CallbackTypes", SyncCallback, AsyncCallback)
