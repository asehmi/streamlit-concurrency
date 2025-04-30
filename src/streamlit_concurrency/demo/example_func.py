import os
import numpy as np
import time
import datetime
import asyncio
import streamlit_concurrency as stc
from streamlit_concurrency._func_util import globalize


@stc.run_in_executor(executor="process")
def sync_cpu_intensive_in_process_executor(n: int):
    """A CPU-intensive task that takes a long time to compute."""
    result = 0
    for i in range(n):
        result += i**2
    return f"i ** {n} = {result} computed by {sync_cpu_intensive_in_process_executor.__name__} in pid={os.getpid()}"


@stc.run_in_executor(executor="process")
@globalize
async def async_cpu_intensive_task_in_process_executor(n: int):
    """A CPU-intensive task that takes a long time to compute."""
    result = 0
    for i in range(n):
        result += i**2
    return f"i ** {n} = {result} computed by {sync_cpu_intensive_in_process_executor.__name__} in pid={os.getpid()}"


def cpu_heavy_sync(run_for_seconds: int, size=1000):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=run_for_seconds)
    while datetime.datetime.now() < deadline:
        np.random.rand(size, size)
        time.sleep(0)


def sleep_sync(seconds: int):
    time.sleep(seconds)


async def cpu_heavy_async(delay: int, size=1000):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=delay)
    while datetime.datetime.now() < deadline:
        await asyncio.to_thread(np.random.rand, size, size)


async def sleep_async(seconds: float):
    await asyncio.sleep(seconds)
