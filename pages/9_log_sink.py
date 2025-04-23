import streamlit as st
import streamlit.logger as stl
from streamlit_concurrency.demo.log_sink import test_log_sink

run = st.button("Run Log Sink Test")
dest = st.empty()

if run:
    test_log_sink()
else:
    dest.write("Click the button to capture log the test.")
