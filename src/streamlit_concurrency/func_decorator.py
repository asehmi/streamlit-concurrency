from concurrent.futures import Executor
from streamlit.runtime.caching.hashing import HashFuncsDict
import concurrent.futures as cf
from typing import (
    Awaitable,
    Literal,
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

from ._executors import _get_thread_pool_executor, _get_process_pool_executor

R = TypeVar("R")
P = ParamSpec("P")


def wrap_sync(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | Literal["thread_pool", "process_pool"] = "thread_pool",
    with_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:
    """Transforms a sync function to run in executor and return result as Awaitable

    @param cache_key: cache key
    @param cache_storage: cache storage
    @param cache_ttl: cache ttl
    @param hash_funcs: hash functions
    @param executor: executor to run the function in, can be 'thread_pool', 'process_pool' or an concurrent.futures.Executor
    @param with_script_run_context: if True, the function will be run with a ScriptRunContext.
    With a ScriptRunContext it will be able to call specific streamlit APIs.
    Must be used with a ThreadPoolExecutor.


    """
    if executor == "thread_pool":
        executor = _get_thread_pool_executor()
    elif executor == "process_pool":
        executor = _get_process_pool_executor()
    elif not isinstance(executor, cf.Executor):
        raise ValueError(
            f"executor must be 'thread_pool', 'process_pool' or an instance of concurrent.futures.Executor, got {executor}"
        )

    if with_script_run_context and not isinstance(executor, cf.ThreadPoolExecutor):
        raise ValueError(
            "with_script_run_context=True can only be used with a ThreadPoolExecutor"
        )

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
