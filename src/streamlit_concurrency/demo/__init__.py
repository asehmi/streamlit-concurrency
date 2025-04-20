import streamlit as st
import numpy as np
import time
import datetime
import asyncio
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent


def render_page_src(page_file: str):
    with st.expander("Source code", expanded=False):
        code = get_page_code(page_file)
        st.code(code, language="python", line_numbers=True)
    st.markdown(f"View source code on [GitHub]({to_github_url(page_file)})")


def get_page_code(page_file: str) -> str:
    """
    Read the content of the page file and return it as a string.
    """
    with open(page_file, "r") as f:
        code = f.read()
    return code


def to_github_url(page_file: str) -> str:
    github_tree = "https://github.com/jokester/streamlit-concurrency/tree/main"
    path_in_repo = Path(page_file).relative_to(REPO_ROOT)
    return f"{github_tree}/{path_in_repo}"


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
