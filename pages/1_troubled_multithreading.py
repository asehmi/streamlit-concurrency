import streamlit as st
import threading
import time
import streamlit_concurrency.demo as demo

st.markdown("""
This page demostrates incorrect use of multithreading in streamlit.
            
Please click a button and check exceptions and warnings in the console.
""")

st.session_state["foo"] = "foo-value"

update_widget_clicked = st.button(f"Update widget in a new thread")

read_session_state_clicked = st.button("Read session state in a new thread")

result = st.empty()

st.divider()
demo.render_page_src(__file__)


@st.cache_data()
def get_data():
    return "dummy"


class CustomThreadUpdatingWidget(threading.Thread):
    def run(self):
        # sleeping
        time.sleep(2)
        # a custom thread can call @st.cache_data() function
        data = get_data()
        assert data == "dummy"

        # but updating a widget in a custom thread will throw `streamlit.errors.NoSessionContext`
        result.write(data)


class CustomThreadReadingSessionState(threading.Thread):
    def run(self):
        value = st.session_state.get("foo", None)
        assert value is None, "Session state should be None in a new thread"
        time.sleep(2)
        print(
            f"st.session_state['foo'] as seen by {threading.current_thread().name} is {value}"
        )


if update_widget_clicked:
    t = CustomThreadUpdatingWidget()
    t.start()
elif read_session_state_clicked:
    t = CustomThreadReadingSessionState()
    t.start()
