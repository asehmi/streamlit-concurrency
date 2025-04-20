import pytest
from .func_decorator import wrap_async, wrap_sync


@pytest.mark.asyncio
async def test_sync_1():
    @wrap_sync()
    def f(x: int, y: int) -> int:
        return x + y

    assert await f(1, 2) == 3
