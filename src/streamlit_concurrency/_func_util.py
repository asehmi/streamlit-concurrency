import inspect
import sys
import uuid
import contextlib
import logging
import time
from ._errors import UnsupportedFunction


logger = logging.getLogger(__name__)


def assert_is_transformable_async(func):
    """Asserts that the given function is an async function."""
    if not callable(func):
        raise UnsupportedFunction(f"Expected a callable, got {func}.")
    if not inspect.iscoroutinefunction(func):
        # Check if the function is a coroutine function
        raise UnsupportedFunction(f"Expected an async function, got {func.__code__}.")
    if inspect.isasyncgenfunction(func):
        raise UnsupportedFunction(
            f"Expected an non-generator function, got {func.__code__}."
        )


def assert_is_transformable_sync(func):
    """Asserts that the given function is an async function."""
    if not callable(func):
        raise UnsupportedFunction(f"Expected a callable, got {func}.")
    if inspect.iscoroutinefunction(func):
        # Check if the function is a coroutine function
        raise UnsupportedFunction(f"Expected a sync function, got {func.__code__}.")
    if inspect.isgeneratorfunction(func):
        raise UnsupportedFunction(
            f"Expected an non-generator function, got {func.__code__}."
        )


@contextlib.contextmanager
def debug_enter_exit(logger_: logging.Logger, enter_msg: str, exit_msg):
    enter_at = time.time()
    logger_.debug(enter_msg)
    yield
    exit_at = time.time()
    logger_.debug(exit_msg + " (took %.2f seconds)", exit_at - enter_at)


# a hack to make a (possibly inner) function module-global
# stole from https://gist.github.com/EdwinChan/3c13d3a746bb3ec5082f
# but not working for cf.ProcessPoolExecutor


def globalize(func):
    def result(*args, **kwargs):
        return func(*args, **kwargs)

    result.__name__ = result.__qualname__ = uuid.uuid4().hex
    setattr(sys.modules[result.__module__], result.__name__, result)
    return result
