import functools
import concurrent.futures as cf
from typing import Literal
from ._func_util import debug_enter_exit
import threading

import logging

logger = logging.getLogger(__name__)

# just to be safe
_get_executor_lock = threading.Lock()


@functools.lru_cache(maxsize=1)
def _get_thread_pool_executor() -> cf.Executor:
    with debug_enter_exit(
        logger, "Creating ThreadPoolExecutor", "Created ThreadPoolExecutor"
    ):
        return cf.ThreadPoolExecutor(thread_name_prefix="streamlit-concurrency")


@functools.lru_cache(maxsize=1)
def _get_process_pool_executor() -> cf.Executor:
    raise NotImplementedError


@functools.lru_cache(maxsize=1)
def _get_interpreter_pool_executor() -> cf.Executor:
    # should be available since py3.14
    return cf.InterpreterPoolExecutor()


@functools.lru_cache(maxsize=1)
def _get_multiprocess_executor() -> cf.Executor:
    raise NotImplementedError


def get_executor(
    executor_type: Literal["thread", "process", "interpreter"],
) -> cf.Executor:
    """Get the executor based on the type."""
    with _get_executor_lock:
        if executor_type == "thread":
            return _get_thread_pool_executor()
        elif executor_type == "process":
            return _get_process_pool_executor()
        elif executor_type == "interpreter":
            return _get_interpreter_pool_executor()
        else:
            raise ValueError(f"Unknown executor type: {executor_type}")
