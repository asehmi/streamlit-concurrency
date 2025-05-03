import pytest
from ._decorator_sync import transform_sync
from .demo import example_func
from ._decorator_async import transform_async
from ._errors import UnsupportedExecutor, UnsupportedFunction, UnsupportedCallSite
from ._streamlit_hack import _strict_get_ctx, _prohibit_get_ctx
from ._streamlit_util import has_streamlit_server
from ._executors import get_executor
import streamlit.runtime.scriptrunner as st_scriptrunner


def module_top_function():
    pass


def test_assertions():
    with pytest.raises(UnsupportedFunction):
        transform_async(example_func.sleep_sync, executor=get_executor("thread"))  # type: ignore

    with pytest.raises(UnsupportedFunction):
        transform_sync(example_func.sleep_async, executor=get_executor("thread"))

    with pytest.raises(UnsupportedCallSite):
        _strict_get_ctx()

    with pytest.raises(UnsupportedCallSite):
        _prohibit_get_ctx()

    assert has_streamlit_server() is False


def test_importable_function():
    def inner_function(): ...

    with pytest.raises(UnsupportedFunction):
        transform_sync(inner_function, executor=get_executor("process"))

    with pytest.raises(UnsupportedFunction):
        transform_sync(lambda l: 2, executor=get_executor("process"))

    transform_sync(module_top_function, executor=get_executor("process"))


def test_without_monkeypatch():
    st_scriptrunner.get_script_run_ctx(suppress_warning=False)


def test_stricter(stricter_get_run_ctx, stub_run_ctx_cm):
    with pytest.raises(UnsupportedCallSite):
        st_scriptrunner.get_script_run_ctx(suppress_warning=True)
    with stub_run_ctx_cm:
        st_scriptrunner.get_script_run_ctx(suppress_warning=True)


def test_prohibit(prohibit_get_run_ctx, stub_run_ctx_cm):
    with pytest.raises(UnsupportedCallSite):
        st_scriptrunner.get_script_run_ctx(suppress_warning=True)
    with stub_run_ctx_cm:
        with pytest.raises(UnsupportedCallSite):
            st_scriptrunner.get_script_run_ctx(suppress_warning=True)
