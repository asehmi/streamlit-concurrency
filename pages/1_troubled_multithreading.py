import streamlit as st
import logging
import threading
import time
import streamlit_concurrency.demo as demo
from streamlit_concurrency.log_sink import create_log_sink

st.markdown("""
This page demostrates incorrect multithreading in streamlit.
            
Please click a button and observe this page and the console.
""")

st.session_state["foo"] = "foo-value"

update_widget_clicked = st.button(f"Update widget in a new thread")

read_session_state_clicked = st.button("Read session state in a new thread")

# won't be updated actually
result = st.empty()

st.divider()
demo.render_page_src(__file__)


@st.cache_data()
def get_data():
    return "dummy"


class CustomThreadUpdatingWidget(threading.Thread):
    def run(self):
        # sleeping
        time.sleep(1)
        # a custom thread can call @st.cache_data() function
        data = get_data()
        assert data == "dummy"

        # but updating a widget in a custom thread will throw `streamlit.errors.NoSessionContext`
        result.write(data)


class CustomThreadReadingSessionState(threading.Thread):
    def run(self):
        value = st.session_state.get("foo", None)
        assert value is None, "Session state should be None in a new thread"
        time.sleep(1)
        print(
            f"st.session_state['foo'] as seen by {threading.current_thread().name} is {value}"
        )


# NOTE this does not capture errors
with create_log_sink(level=logging.DEBUG) as (records, lines):
    if update_widget_clicked:
        t = CustomThreadUpdatingWidget()
        t.start()
        t.join()
    elif read_session_state_clicked:
        t = CustomThreadReadingSessionState()
        t.start()
        t.join()
