from typing import (
    TypeVar,
    Callable,
    Awaitable,
    overload,
    ParamSpec,
    ParamSpecArgs,
    ParamSpecKwargs,
    TypedDict,
)

R = TypeVar("R")
P = ParamSpec("P")
