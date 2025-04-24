import pytest
from ._decorator_sync import transform_sync
from .demo import example_func
from ._decorator_async import transform_async
from ._errors import UnsupportedExecutor, UnsupportedFunction, UnsupportedCallSite
from ._test_hack import _strict_get_ctx, _prohibit_get_ctx


def test_assertions():
    with pytest.raises(UnsupportedFunction):
        transform_async(example_func.sleep_sync)  # type: ignore

    with pytest.raises(UnsupportedFunction):
        transform_sync(example_func.sleep_async)

    with pytest.raises(UnsupportedCallSite):
        _strict_get_ctx()

    with pytest.raises(UnsupportedCallSite):
        _prohibit_get_ctx()
