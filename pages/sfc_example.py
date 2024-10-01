import time
import streamlit as st
import streamlit_concurrency as stc

st.title("streamlit-concurrency demo")

@stc.run_in_executor(copy_script_run_context=True, cache_size=1)
def slow_function():
    time.sleep(5)
    return "done"

v = slow_function()

v