"""Workaround for "inner function" case in https://github.com/streamlit/streamlit/issues/11157"""

import streamlit as st
from streamlit.runtime.caching.cache_type import CacheType
from streamlit.runtime.caching.cache_utils import _make_function_key


def create_cached_inner_function(a: int):
    def inner_function(b: int):
        return f"a={a} b={b}"

    orig_qualname = inner_function.__qualname__
    # this allows _make_function_key to distinguish between inner functions captured different a-s
    inner_function.__qualname__ += f" captured a={a}"

    return (
        orig_qualname,
        _make_function_key(CacheType.DATA, inner_function),
        st.cache_data(inner_function),
    )


orig_qn1, key1, cached_func1 = create_cached_inner_function(1)
orig_qn2, key2, cached_func2 = create_cached_inner_function(2)

assert orig_qn1 == orig_qn2
assert key1 != key2

st.write(f"orig_qn: {orig_qn1}")

st.write(f"create_cached_inner_function(1)(1): {key1} / {repr(cached_func1(1))}")
st.write(f"create_cached_inner_function(2)(1): {key2} / {repr(cached_func2(1))}")
