import inspect
from streamlit.runtime.scriptrunner import get_script_run_ctx, ScriptRunContext


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
