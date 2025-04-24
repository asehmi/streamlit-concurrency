import pytest
import logging
import asyncio
from .func_decorator import run_in_executor
import streamlit.runtime.scriptrunner as st_scriptrunner
from .log_sink import create_log_sink
from ._errors import UnsupportedCallSite


logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_sync_simple(prohibit_get_run_ctx):
    @run_in_executor()
    def f(x: int, y: int) -> int:
        logger.info("f called with x=%s y=%s", x, y)
        return x + y

    with create_log_sink(logger_names=frozenset([__name__])) as (records, lines):
        assert await f(1, 2) == 3
    logged_args = [
        rec.args
        for rec in records
        if rec.msg == "f called with x=%s y=%s"
        and rec.threadName.startswith("streamlit-concurrency")  # type: ignore
    ]
    assert logged_args == [(1, 2)]


@pytest.mark.asyncio
async def test_sync_with_script_run_context(stub_run_ctx_cm):
    @run_in_executor(with_script_run_context=True)
    def foo(x: int, y: int) -> int:
        ctx = st_scriptrunner.get_script_run_ctx()
        assert ctx is not None
        return x + y

    # transformed foo cannot be called without a ScriptRunContext
    with pytest.raises(UnsupportedCallSite):
        await foo(1, 2)

    # transformed foo can be called with a stub ScriptRunContext
    with stub_run_ctx_cm:
        assert await foo(1, 2) == 3


@pytest.mark.asyncio
async def test_sync_cached(prohibit_get_run_ctx):
    @run_in_executor(cache={"ttl": 0.2})
    def foo(param: int):
        logger.info("foo called %s", param)
        return param

    with create_log_sink(logger_names=[__name__]) as (records, lines):
        assert await foo(1) == 1
        assert await foo(1) == 1  # cache hit
        assert await foo(2) == 2
        await asyncio.sleep(0.2)
        assert await foo(1) == 1  # cache miss after TTL

    args = [
        r.args
        for r in records
        if r.threadName.startswith("streamlit-concurrency") and r.msg == "foo called %s"  # type: ignore
    ]

    assert args == [(1,), (2,), (1,)]


@pytest.mark.asyncio
async def test_sync_cached_inner_function(prohibit_get_run_ctx):
    def create_foo():
        @run_in_executor(cache={"ttl": 0.2})
        def foo(param: int):
            logger.info("foo called %s", param)
            return param

        return foo

    foo1 = create_foo()
    foo2 = create_foo()

    with create_log_sink(logger_names=frozenset([__name__])) as (records, lines):
        assert await foo1(1) == 1
        assert await foo2(1) == 1  # cache hit
        assert await foo1(2) == 2
        await asyncio.sleep(0.2)
        assert await foo1(1) == 1  # cache miss after TTL

    logged_args = [
        r.args
        for r in records
        if r.threadName.startswith("streamlit-concurrency") and r.msg == "foo called %s"  # type: ignore
    ]

    assert logged_args == [(1,), (2,), (1,)]
