import os
import streamlit as st
import streamlit_concurrency as stc
# Like thi


@stc.run_in_executor(executor="process")
def cpu_intensive_task(n: int):
    """A CPU-intensive task that takes a long time to compute."""
    result = 0
    for i in range(n):
        result += i**2
    return f"i ** {n} = {result} computed by {cpu_intensive_task.__name__} in pid={os.getpid()}"


@stc.run_in_executor(executor="process")
async def async_cpu_intensive_task(n: int):
    """A CPU-intensive task that takes a long time to compute."""
    result = 0
    for i in range(n):
        result += i**2
    return f"i ** {n} = {result} computed by {cpu_intensive_task.__name__} in pid={os.getpid()}"
