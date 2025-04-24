import asyncio
import concurrent.futures as cf
import streamlit as st
import functools
import contextlib
import logging

from typing import (
    Coroutine,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
)
from ._func_util import (
    assert_is_transformable_async,
    debug_enter_exit,
)
from ._streamlit_util import (
    assert_st_script_run_ctx,
    create_script_run_context_cm,
)
from ._func_cache import CacheConf
from ._executors import get_executor

R = TypeVar("R")
P = ParamSpec("P")
logger = logging.getLogger(__name__)


def transform_async(
    func: Callable[P, Coroutine[None, None, R]],
    cache: Optional[CacheConf | dict] = None,
    executor: cf.Executor | Literal["thread", "process"] = "thread",
    with_script_run_context: bool = False,
) -> Callable[P, Coroutine[None, None, R]]:
    """Transforms a *async* function to do real work in executor

    @param cache: configuration to pass to st.cache_data()

    @param executor: executor to run the function in

    @param with_script_run_context: if True, the thread running provided function will be run with a ScriptRunContext.

    See [multithreading](https://docs.streamlit.io/develop/concepts/design/multithreading) for possible motivation and consequences.
    This option must be used with a ThreadPoolExecutor.

    @return: an async function

    """
    assert executor == "thread"
    assert_is_transformable_async(func)

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

    waiter_executor = get_executor("thread")

    async def wrapper(*args, **kwargs) -> R:
        if with_script_run_context:
            cm = create_script_run_context_cm(
                assert_st_script_run_ctx(
                    f"<@run_in_executor(..) async def {func.__name__}>"
                )
            )
        else:
            cm = contextlib.nullcontext()

        # the sync function to do real work in the executor, and in an 'clean' thread without an event loop
        def run_in_executor(*args, **kwargs) -> R:
            f"""dispatched for {func.__code__}"""
            with cm:
                with debug_enter_exit(
                    logger,
                    f"executing original {func.__name__}",
                    f"executed original {func.__name__}",
                ):
                    return asyncio.run(func(*args, **kwargs))

        def cachable_run_in_executor(*args, **kwargs) -> R:
            with debug_enter_exit(
                logger,
                f"waiting for {run_in_executor.__name__} wrapping {func.__name__}",
                f"waited for {run_in_executor.__name__} wrapping {func.__name__}",
            ):
                return executor.submit(run_in_executor, *args, **kwargs).result()

        # this hack is required for st.cache to create different cache key for each run_in_executor instance
        # see https://github.com/streamlit/streamlit/issues/11157
        cachable_run_in_executor.__qualname__ += f" wrapping {func.__qualname__}"

        # dispatch run_in_executor (now cacheable with st.cache_data) to the (worker) executor
        def run_with_cache_in_waiter_executor(*args, **kwargs) -> R:
            if cache is None:
                future = waiter_executor.submit(run_in_executor, *args, **kwargs)
                return future.result()

            # else: wrap with st.cache_data first
            with cm:
                run_in_executor_with_cache = st.cache_data(run_in_executor, **cache)
            with debug_enter_exit(
                logger,
                f"waiting for cached {func.__name__}",
                f"waiting for cached {func.__name__}",
            ):
                future = executor.submit(run_in_executor_with_cache, *args, **kwargs)
                return run_in_executor_with_cache(*args, **kwargs)

        return await run_with_cache_in_waiter_executor(*args, **kwargs)

    return functools.update_wrapper(wrapper, func)
