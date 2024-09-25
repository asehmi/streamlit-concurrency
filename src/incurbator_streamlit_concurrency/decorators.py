from functools import singledispatch
from typing import Callable, Optional, TypedDict, Union
from concurrent.futures import Executor


class Param(TypedDict):
    executor: Optional[Union[str, Executor]]
    cache_session: Optional[bool]
    cache_global: Optional[bool]
    cache_size: Optional[int]


@singledispatch
def run_in_worker_thread(
    maybe_callable: Optional[Callable] = None, **kwargs
) -> Callable:
    raise AssertionError("should not be here")


@run_in_worker_thread.register
def impl_none(none: None, **kwargs) -> Callable:
    return lambda callable: _wrapper(callable, **kwargs)


@run_in_worker_thread.register
def impl_callable(callable: Callable, **kwargs) -> Callable:
    return _wrapper(callable, **kwargs)


def _wrapper(f: Callable, **kwargs):
    return f
