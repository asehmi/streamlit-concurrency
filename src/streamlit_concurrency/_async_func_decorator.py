import streamlit as st
from typing import (
    Awaitable,
    Literal,
    Optional,
    TypeVar,
    Callable,
    ParamSpec,
    overload,
)

R = TypeVar("R")
P = ParamSpec("P")

from ._func_cache import CacheConf
from ._func_util import assert_is_sync, assert_is_async


def wrap_async(
    cache: Optional[CacheConf | dict] = None,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        assert_is_async(func)

        def wrapper(*args, **kwargs):
            if cache is not None:
                # st.cache_data needs the real user function
                # its cache key depends on code position and code text
                real_func = st.cache_data(func, **cache)
            else:
                real_func = func

            return real_func(*args, **kwargs)

        return wrapper

    return decorator
