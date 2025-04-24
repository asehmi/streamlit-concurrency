import streamlit as st
import itertools
import streamlit.logger as stl
from streamlit_concurrency.log_sink import create_log_sink
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


if run:
    test_log_sink()
else:
    dest.write("Click the button to capture log the test.")
