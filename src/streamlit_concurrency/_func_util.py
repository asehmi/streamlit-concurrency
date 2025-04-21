import inspect
import contextlib
import threading

from streamlit.runtime.scriptrunner import (
    get_script_run_ctx,
    add_script_run_ctx,
    ScriptRunContext,
)
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)


def assert_has_script_thread() -> ScriptRunContext:
    """Assert that the current thread is the script thread."""
    ctx = get_script_run_ctx(suppress_warning=True)
    if ctx is None:
        raise RuntimeError("This function must be called in a Streamlit script.")
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


@contextlib.contextmanager
def create_script_run_context_cm(script_run_ctx: ScriptRunContext):
    """Create a context manager that

    - when entering, adds given script_run_ctx to the current thread
    - when exiting, un-adds it from current thread
    """
    existing_ctx = get_script_run_ctx(suppress_warning=True)

    if existing_ctx is not None and existing_ctx is not script_run_ctx:
        raise RuntimeError(
            f"Current thread {threading.current_thread().name} had an unexpected ScriptRunContext: {existing_ctx}."
        )

    add_script_run_ctx(thread=threading.current_thread(), ctx=script_run_ctx)
    yield

    # restore the original context, whether it was None or not (this can't be done with add_script_run_ctx)
    setattr(threading.current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, existing_ctx)
    assert get_script_run_ctx(suppress_warning=True) is existing_ctx
