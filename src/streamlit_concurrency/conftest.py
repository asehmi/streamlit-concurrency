import pytest
from ._test_hack import patch_st_get_ctx


@pytest.fixture
def stricter_get_ctx():
    """Fixture to patch get_script_run_ctx to be stricter about its use."""
    patch_st_get_ctx(strict=True)
    yield
    patch_st_get_ctx()


@pytest.fixture
def prohibit_get_ctx():
    """Fixture to patch get_script_run_ctx to be stricter about its use."""
    patch_st_get_ctx(prohibit=True)
    yield
    patch_st_get_ctx()
