import asyncio
import concurrent.futures as cf
import streamlit as st
import functools
import contextlib
from ._func_util import (
    async_to_sync,
    assert_st_script_run_ctx,
    create_script_run_context_cm,
    dump_func_metadata,
    dump_func_code,
)
from concurrent.futures import Executor
import logging

from typing import (
    Awaitable,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
)
from ._func_cache import CacheConf
from ._func_util import assert_is_async
from ._executors import get_executor

logger = logging.getLogger(__name__)

R = TypeVar("R")
P = ParamSpec("P")


def wrap_async(
    cache: Optional[CacheConf | dict] = None,
    executor: Executor | Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    assert executor == "thread"
    if isinstance(executor, str):
        executor = get_executor(executor)
    if not isinstance(executor, cf.Executor):
        raise ValueError(
            f"executor must be 'thread', 'process' or an instance of concurrent.futures.Executor, got {executor}"
        )
    threaded_executor = executor

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        assert_is_async(func)

        dump_func_metadata(func)
        dump_func_code("wrap_async-func", func)

        def wrapper(*args, **kwargs) -> Awaitable[R]:
            if with_script_run_context:
                cm = create_script_run_context_cm(assert_st_script_run_ctx())
            else:
                cm = contextlib.nullcontext()

            # the sync function to run in the executor
            def dispatched(*args, **kwargs) -> R:
                with cm:
                    return async_to_sync(func)(*args, **kwargs)

            # the sync function that return the result without unpickable container like cf Task/Future or asyncio Task / Future
            def dispatch_and_wait(*args, **kwargs) -> R:
                f"""{func.__name__} {func.__code__}"""
                return executor.submit(dispatched, *args, **kwargs).result()

            dispatch_and_wait = functools.update_wrapper(dispatch_and_wait, func)

            dump_func_code("wrap_async-dispatch", dispatch_and_wait)

            if cache is not None:
                # st.cache_data needs the real user function
                # its cache key depends on code position and code text
                real_func = st.cache_data(dispatch_and_wait, **cache)
            else:
                real_func = dispatch_and_wait

            future = executor.submit(real_func, *args, **kwargs)
            return asyncio.wrap_future(future)

        return wrapper

    return decorator
