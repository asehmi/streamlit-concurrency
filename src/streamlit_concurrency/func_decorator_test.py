import pytest
import time
import asyncio
import logging

from .func_decorator import run_in_executor
from ._errors import UnsupportedExecutor, UnsupportedFunction, UnsupportedCallSite

logger = logging.getLogger(__name__)


def test_illegal_options():
    with pytest.raises(UnsupportedExecutor):
        run_in_executor(executor="foo")  # type: ignore
    with pytest.raises(ValueError):
        run_in_executor(cache={"show_spinner": True})


@pytest.mark.asyncio
async def test_sync_simple(prohibit_get_run_ctx):
    @run_in_executor()
    def f(x: int, y: int) -> int:
        return x + y

    assert await f(1, 2) == 3


@pytest.mark.asyncio
async def test_sync_with_script_run_context(stub_run_ctx_cm):
    @run_in_executor(with_script_run_context=True)
    def f(x: int, y: int) -> int:
        return x + y

    with pytest.raises(UnsupportedCallSite):
        await f(1, 2)

    with stub_run_ctx_cm:
        assert await f(1, 2) == 3


@pytest.mark.asyncio
async def test_sync_cached(prohibit_get_run_ctx):
    sum = 0

    @run_in_executor(cache={"ttl": 1, "show_spinner": False})
    def inc(delta: int):
        nonlocal sum
        sum += delta
        time.sleep(0.2)

    assert sum == 0
    await inc(1)
    assert sum == 1
    await inc(2)
    assert sum == 3
    await inc(1)  # cache hit and bypassed
    assert sum == 3
    await asyncio.sleep(1)
    await inc(1)
    assert sum == 4
