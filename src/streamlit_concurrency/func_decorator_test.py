import pytest
import asyncio

from .func_decorator import run_in_executor
from ._decorator_sync import transform_sync
from ._decorator_async import transform_async
from .demo import example_func
from ._test_hack import _strict_get_ctx, _prohibit_get_ctx
from ._errors import UnsupportedExecutor, UnsupportedFunction, UnsupportedCallSite


def test_assertions():
    with pytest.raises(UnsupportedFunction):
        transform_async(example_func.sleep_sync)  # type: ignore

    with pytest.raises(UnsupportedFunction):
        transform_sync(example_func.sleep_async)

    with pytest.raises(UnsupportedCallSite):
        _strict_get_ctx()

    with pytest.raises(UnsupportedCallSite):
        _prohibit_get_ctx()


@pytest.mark.asyncio
async def test_sync_1():
    @run_in_executor()
    def f(x: int, y: int) -> int:
        return x + y

    assert await f(1, 2) == 3


@pytest.mark.asyncio
async def test_sync_cached(prohibit_get_ctx):
    sum = 0

    @run_in_executor(cache={"ttl": 1})
    def inc(delta: int):
        nonlocal sum
        sum += delta

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
