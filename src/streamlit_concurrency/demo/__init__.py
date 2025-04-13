import numpy as np
import time
import datetime
import asyncio


def cpu_heavy_sync(delay: int, size=1000):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=delay)
    while datetime.datetime.now() < deadline:
        np.random.rand(size, size)


def sleep_sync(seconds: int):
    time.sleep(seconds)


async def cpu_heavy_async(delay: int, size=1000):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=delay)
    while datetime.datetime.now() < deadline:
        await asyncio.to_thread(np.random.rand, size, size)


async def sleep_async(seconds: float):
    await asyncio.sleep(seconds)
