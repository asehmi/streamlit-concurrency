"""_summary_"""

from concurrent.futures import Executor
from streamlit.runtime.caching.hashing import HashFuncsDict
import concurrent.futures as cf
from typing import (
    Awaitable,
    TypeVar,
    Callable,
    ParamSpec,
    TypedDict,
    Unpack,
    Any,
)
import asyncio
from ._func_util import assert_is_async, assert_is_sync, assert_has_script_thread

from ._executors import _get_thread_pool_executor

R = TypeVar("R")
P = ParamSpec("P")


async def _run_sync_in_executor(
    ex: Executor, sync_func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
) -> R:
    future: cf.Future[R] = ex.submit(sync_func, *args, **kwargs)
    res: R = await asyncio.wrap_future(future)
    return res


def wrap_sync(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | None = None,
    copy_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:
    """Transforms a sync function into an async function, with st-aware helpers"""
    if executor is None:
        executor = _get_thread_pool_executor()

    def decorator(func: Callable):
        assert_is_sync(func)

        def wrapper(*args, **kwargs):
            # TODO: capture bindings to caller context
            return _run_sync_in_executor(executor, func, *args, **kwargs)

        return wrapper

    return decorator


def wrap_future(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | None = None,
    copy_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, cf.Future[R]]]:
    """Transforms a sync function into a sync function running in , with st helpers"""
    raise NotImplementedError


def wrap_async(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | None = None,
    copy_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """XXX: is this ever necessary?"""
    raise NotImplementedError
