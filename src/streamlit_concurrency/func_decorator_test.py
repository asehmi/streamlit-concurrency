import pytest
from .func_decorator import wrap_async, wrap_sync
import asyncio


@pytest.mark.asyncio
async def test_sync_1():
    @wrap_sync()
    def f(x: int, y: int) -> int:
        return x + y

    assert await f(1, 2) == 3


@pytest.mark.asyncio
async def test_sync_cached():
    sum = 0

    @wrap_sync(cache={"ttl": 1})
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
