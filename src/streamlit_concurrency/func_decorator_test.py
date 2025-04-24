import pytest
import logging

from .func_decorator import run_in_executor
from ._errors import UnsupportedExecutor

logger = logging.getLogger(__name__)


def test_illegal_options():
    with pytest.raises(UnsupportedExecutor):
        run_in_executor(executor="foo")  # type: ignore
    with pytest.raises(ValueError):
        run_in_executor(cache={"show_spinner": True})
