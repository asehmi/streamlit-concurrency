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

R = TypeVar("R")
P = ParamSpec("P")


def wrap_sync(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | None = None,
    copy_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, Awaitable[R]]]:
    """Transforms a sync function into an async function, with st helpers"""
    raise NotImplementedError


def wrap_future(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | None = None,
    copy_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, cf.Future[R]]]:
    """Transforms a sync function into an async function, with st helpers"""
    raise NotImplementedError


def wrap_async(
    cache_key: str | None = None,
    cache_storage: str | None = None,
    cache_ttl: int | None = None,
    hash_funcs: HashFuncsDict | None = None,
    executor: Executor | None = None,
    copy_script_run_context: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    raise NotImplementedError
