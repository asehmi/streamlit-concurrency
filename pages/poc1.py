import asyncio
import streamlit as st
import streamlit_concurrency.demo as demo
import datetime
import threading

dest1 = st.empty()
dest2 = st.empty()


async def async1(dest, interval: float, stop_after: float):
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=stop_after)
    while datetime.datetime.now() < deadline:
        await asyncio.sleep(interval)
        dest.write(datetime.datetime.now())


async def main():
    run_clicked = st.button("Run")

    if run_clicked:
        await asyncio.gather(
            async1(dest1, 1.1, 10),
            async1(dest2, 1.2, 10),
        )


asyncio.run(main())
