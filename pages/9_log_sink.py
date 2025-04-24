import asyncio
import streamlit as st
import itertools
import streamlit.logger as stl
from streamlit_concurrency.log_sink import create_log_sink
from streamlit_concurrency.demo import capture_logs_render_df
import logging

logger = logging.getLogger(__name__)
run = st.button("Run Log Sink Test")
dest = st.empty()


def test_log_sink():
    with create_log_sink() as (log_records, log_lines):
        logger.warning("test")
        logger.warning("test2")

    for rec, line in itertools.zip_longest(log_records, log_lines):
        print(rec, "=>", line)


async def emit_logs():
    for i in range(5):
        logger.warning("test %d", i)
        await asyncio.sleep(0.1)


async def main():
    await asyncio.gather(capture_logs_render_df(dest, 5, 0.1), emit_logs())


if run:
    asyncio.run(main())
else:
    dest.write("Click the button to capture log the test.")
