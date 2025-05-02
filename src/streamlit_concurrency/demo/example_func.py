import os
import numpy as np
import time
import datetime
import asyncio
from streamlit_concurrency import run_in_executor


def cpu_intensive_computation(n: int) -> tuple[int, int]:
    """A CPU-intensive task that takes a long time to compute."""
    result = 0
    for i in range(n):
        result += i**2
    return result, os.getpid()


cpu_intensive_computation_in_process_executor = run_in_executor(
    executor="process",
    cache={
        "ttl": 5,
        "max_entries": 3,
    },
)(cpu_intensive_computation)


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
