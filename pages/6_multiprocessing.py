import os
import asyncio
import streamlit as st
from streamlit_concurrency.demo import example_func
# Like thi

st.write(f"Streamlit app pid: {os.getpid()}")

dest = st.empty()


async def main():
    dest.markdown(f"""
res1: running...

res2: running...
""")
    res1, res2 = await asyncio.gather(
        example_func.sync_cpu_intensive_in_process_executor(1000),
        example_func.sync_cpu_intensive_in_process_executor(1000),
    )
    dest.markdown(f"""
res1: {res1}

res2: {res2}
""")


asyncio.run(main())
