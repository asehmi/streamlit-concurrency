import inspect
import asyncio
import contextlib
import threading
import logging
from typing import Callable, Optional
import os


from streamlit.runtime.scriptrunner import (
    get_script_run_ctx,
    add_script_run_ctx,
    ScriptRunContext,
)
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)

logger = logging.getLogger(__name__)


def assert_st_script_run_ctx(callee: str) -> ScriptRunContext:
    """Assert that the current thread is the script thread."""
    ctx = get_script_run_ctx(suppress_warning=True)
    if ctx is None:
        raise RuntimeError(
            f"{callee} must be called in a thread with ScriptRunContext. Typically a thread streamlit created to run a page."
        )
    return ctx


def assert_is_async(func):
    """Asserts that the given function is an async function."""
    if not (callable(func) and inspect.iscoroutinefunction(func)):
        raise TypeError(f"Expected an async function, got {func}")
    return func


def assert_is_sync(func):
    """Asserts that the given function is an async function."""
    if not (callable(func) and not inspect.iscoroutinefunction(func)):
        raise TypeError(f"Expected an sync function, got {func}")
    return func


def _format_script_run_ctx(ctx: Optional[ScriptRunContext]):
    return (
        f"ScriptRunContext(session={ctx.session_id}, page_script_hash={ctx.page_script_hash})"
        if ctx
        else None
    )


@contextlib.contextmanager
def create_script_run_context_cm(ctx: ScriptRunContext):
    """Create a context manager that

    - when enter, adds given script_run_ctx to the current thread
    - when exit, un-adds it from current thread
    """
    existing_ctx = get_script_run_ctx(suppress_warning=True)
    existing_ctx_repr = _format_script_run_ctx(existing_ctx)

    ctx_repr = _format_script_run_ctx(ctx)
    if existing_ctx is not None and existing_ctx is not ctx:
        raise RuntimeError(
            f"Current thread {threading.current_thread().name} had an unexpected ScriptRunContext: {existing_ctx}."
        )

    add_script_run_ctx(thread=threading.current_thread(), ctx=ctx)
    logger.debug(
        "Attached captured ScriptRunContext %s . Current thread had %s .",
        ctx_repr,
        existing_ctx_repr,
    )
    yield

    # restore the original value, whether it was None or not (this can't be done with add_script_run_ctx)
    setattr(threading.current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, existing_ctx)
    assert get_script_run_ctx(suppress_warning=True) is existing_ctx
    logger.debug("Restored to original ScriptRunContext %s", existing_ctx_repr)


def dump_func_metadata(func: Callable):
    logger.debug(
        "function metadata: %s %s %s",
        func.__module__,
        func.__name__,
        func.__qualname__,
    )
    logger.debug(
        "getsource: %s",
        inspect.getsource(func),
    )


def dump_func_code(callsite: str, func: Callable):
    logger.warning("function code at %s: %s", callsite, func.__code__)


def log_with_callsite(msg: str, *args, **kwargs):
    logger.warning(
        "pid=%s tid=%s thread=%s %s",
        os.getpid(),
        threading.current_thread().ident,
        threading.current_thread().name,
        msg.format(*args, **kwargs),
    )


def async_to_sync(async_fun):
    """Similar to asgiref.sync.async_to_sync, but only supports a 'clean' thread without a event loop."""

    assert inspect.iscoroutinefunction(async_fun)
    assert not inspect.isasyncgenfunction(async_fun)

    def sync_fun(*args, **kwargs):
        return asyncio.run(async_fun(*args, **kwargs))

    return sync_fun


@contextlib.contextmanager
def debug_enter_exit(logger_: logging.Logger, enter_msg: str, exit_msg):
    logger_.debug(enter_msg)
    yield
    logger_.debug(exit_msg)
