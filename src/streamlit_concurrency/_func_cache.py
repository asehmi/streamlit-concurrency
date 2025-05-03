from datetime import timedelta

from typing import TYPE_CHECKING, Callable, Optional, TypedDict, Union

if TYPE_CHECKING:
    from streamlit.runtime.caching.cache_data_api import (
        CachePersistType,
    )
    from streamlit.runtime.caching.hashing import HashFuncsDict


class CacheConf(TypedDict):
    """params for streamlit.cache_data"""

    ttl: float | timedelta | str | None
    max_entries: int | None
    # not suported. Passing in a value will raise
    # show_spinner: Optional[bool]
    persist: Optional[Union["CachePersistType", bool]]
    hash_funcs: Optional["HashFuncsDict"]
    # TODO: maybe use this to provide more exact hash
    # extra_entropy: Union[Hashable, Callable[[], Hashable]]


def st_cache_data(
    func: Callable,
    *,
    persist: Optional[bool] = None,
    ttl: Optional[Union[float, timedelta]] = None,
    max_entries: Optional[int] = None,
    hash_funcs: Optional["HashFuncsDict"] = None,
) -> Callable:
    import streamlit as st

    return st.cache_data(
        persist=persist, ttl=ttl, max_entries=max_entries, hash_funcs=hash_funcs
    )(func)


def st_cache_resource(
    func: Callable,
    *,
    cache: Optional[CacheConf | dict] = None,
    persist: Optional[bool] = None,
    ttl: Optional[Union[float, timedelta]] = None,
    max_entries: Optional[int] = None,
    hash_funcs: Optional["HashFuncsDict"] = None,
) -> Callable:
    import streamlit as st

    # TODO: why no overload matches?
    return st.cache_resource(
        func=func,
        # persist=persist,
        # ttl=ttl,
        # max_entries=max_entries,
        # hash_funcs=hash_funcs,
    )
