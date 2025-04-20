import asyncio
import streamlit as st
import streamlit_concurrency.demo as scdemo
import datetime

st.markdown("""
# single-threaded async

We can concurrently run multiple async functions in a single-threaded event loop, and in 

But if some underlying code is blocking, the whole event loop may be blocked too.
""")

run_clicked = st.button("Run")
dest1 = st.empty()
dest2 = st.empty()


scdemo.render_page_src(__file__)


async def async1(dest, interval: float, stop_after: float):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=stop_after)
    while datetime.datetime.now() < deadline:
        dest.markdown(f"coroutine running: {datetime.datetime.now()}")
        await asyncio.sleep(interval)
    dest.markdown(f"coroutine finished: {datetime.datetime.now()}")


async def main():
    if run_clicked:
        await asyncio.gather(
            async1(dest1, 1.1, 10),
            async1(dest2, 1.2, 10),
        )


asyncio.run(main())
