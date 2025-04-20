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
import contextlib
from streamlit.runtime.scriptrunner import ScriptRunContext
from ._func_util import (
    assert_is_async,
    assert_is_sync,
    assert_has_script_thread,
    create_script_run_context_cm,
)

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
    with_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:
    """Transforms a sync function into an async function, with st-aware helpers"""
    if executor is None:
        executor = _get_thread_pool_executor()

    def decorator(func: Callable):
        assert_is_sync(func)

        def wrapper(*args, **kwargs):
            # a wrapper that
            # 1. capture objects from caller (expectedly a streamlit ScriptThread)
            if with_script_run_context:
                cm = create_script_run_context_cm(assert_has_script_thread())
            else:
                cm = contextlib.nullcontext()

            def func_for_executor():
                with cm:
                    return func(*args, **kwargs)

            future = executor.submit(func_for_executor)
            return asyncio.wrap_future(future)

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
