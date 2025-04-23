import datetime
import asyncio
import streamlit as st
import threading
from streamlit_concurrency import run_in_executor
from streamlit_concurrency.demo import render_page_src


dest = st.container()

run_clicked = st.button("Run main()")


@run_in_executor(
    cache={"ttl": 3},
    with_script_run_context=False,
)
def cached_sync():
    now = datetime.datetime.now()
    # dest.write( f"{now}: {cached_sync.__name__}() running in {threading.current_thread().name}")
    return now


@run_in_executor(
    cache={"ttl": 5},
    with_script_run_context=False,
)
async def cached_async1():
    await asyncio.sleep(1)
    now = datetime.datetime.now()
    # dest.write( f"{now}: {cached_async1.__name__}() running in {threading.current_thread().name}")
    await asyncio.sleep(1)
    return now


@run_in_executor(
    # cache={"ttl": 5},
    with_script_run_context=True,
)
async def cached_async2():
    await asyncio.sleep(1)
    now = datetime.datetime.now()
    dest.write(
        f"{now}: {cached_async2.__name__}() running in {threading.current_thread().name}"
    )
    await asyncio.sleep(1)
    return now


async def main():
    sync_result, async1_result, async2_result = await asyncio.gather(
        cached_sync(), cached_async1(), cached_async2()
    )
    dest.write(f"{cached_sync.__name__}() returned {sync_result}")
    dest.write(f"{cached_async1.__name__}() returned {async1_result}")
    dest.write(f"{cached_async2.__name__}() returned {async2_result}")
    dest.write(
        f"{datetime.datetime.now()}: main() done in script thread {threading.current_thread().name}"
    )


if __name__ == "__main__" and run_clicked:
    asyncio.run(main())


render_page_src(__file__)
