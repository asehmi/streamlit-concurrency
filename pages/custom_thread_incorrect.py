import streamlit as st
import threading
import streamlit_concurrency.demo as scdemo

dest = st.empty()
run_clicked = st.button(
    "Run Thread (and cause `streamlit.errors.NoSessionContext` in terminal)"
)

scdemo.render_page_src(__file__)


@st.cache_data()
def get_data():
    """A function can still be called"""
    return "dummy"


class BadThread(threading.Thread):
    def run(self):
        data = get_data()
        #
        dest.write(data)


if run_clicked:
    t = BadThread()
    t.start()
    t.join()
