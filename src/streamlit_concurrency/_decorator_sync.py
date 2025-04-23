import streamlit as st
import functools
import concurrent.futures as cf
from typing import (
    Awaitable,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
)
import asyncio
import contextlib
import logging
from ._func_util import (
    assert_is_transformable_sync,
    assert_st_script_run_ctx,
    create_script_run_context_cm,
    debug_enter_exit,
)
from ._func_cache import CacheConf
from ._executors import get_executor

R = TypeVar("R")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


def transform_sync(
    func: Callable[P, R],
    cache: Optional[CacheConf | dict] = None,
    executor: cf.Executor | Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> Callable[P, Awaitable[R]]:
    """Transforms a sync function to run in executor and return result as Awaitable

    @param cache: configuration to pass to st.cache_data()

    @param executor: executor to run the function in

    @param with_script_run_context: if True, the thread running provided function will be run with a ScriptRunContext.

    See [multithreading](https://docs.streamlit.io/develop/concepts/design/multithreading) for possible motivation and consequences.
    This option must be used with a ThreadPoolExecutor.

    @return: an async function

    """
    assert_is_transformable_sync(func)

    if isinstance(executor, str):
        executor = get_executor(executor)
    if not isinstance(executor, cf.Executor):
        raise ValueError(
            f"executor must be 'thread', 'process' or an instance of concurrent.futures.Executor, got {executor}"
        )

    if with_script_run_context and not isinstance(executor, cf.ThreadPoolExecutor):
        raise ValueError(
            "with_script_run_context=True can only be used with a ThreadPoolExecutor"
        )

    # dump_func_metadata(func)
    # dump_func_code("wrap_sync", func)

    async def wrapper(*args, **kwargs) -> R:
        # a wrapper that
        # 1. capture possible ScriptRunContext
        # 2. run decorated `func` in executor, with the ScriptRunContext context-managed
        # 3. return a Awaitable
        if with_script_run_context:
            cm = create_script_run_context_cm(
                assert_st_script_run_ctx(f"<@run_in_executor(...) def {func.__name__}>")
            )
        else:
            cm = contextlib.nullcontext()

        # a sync function to do real work in the executor
        def run_in_executor(*args_, **kwargs_):
            # NOTE: need to make sure this works with other executors
            if cache is None:
                with cm:
                    with debug_enter_exit(
                        logger,
                        f"executing original {func.__name__}",
                        f"executed original {func.__name__}",
                    ):
                        return func(*args_, **kwargs_)
            # else: wrap with st.cache_data first
            # NOTE st.cache_data needs the provided user function
            # internally it creates cache key for the function from __module__ __qualname__ __code__ etc
            with cm:
                # NOTE st.cache_data requires ScriptRunContext too (maybe only when show_spinner=True)
                # TODO: validate this and TEST
                func_with_cache = st.cache_data(func, **cache)
            with debug_enter_exit(
                logger,
                f"executing cached {func.__name__}",
                f"executed cached {func.__name__}",
            ):
                return func_with_cache(*args_, **kwargs_)

        future = executor.submit(run_in_executor, *args, **kwargs)
        return await asyncio.wrap_future(future)

    return functools.update_wrapper(wrapper, func)
