import streamlit as st
import threading
import time
import asyncio
import datetime
import streamlit_concurrency.demo as demo
from streamlit_concurrency.func_decorator import wrap_sync

st.markdown("""
This page demostrates multithreading with `streamlit-concurrency`.
            
In this page (compared to `troubled multithreading` page):

1. widget can be updated from an executor thread
2. session state can be accessed in an executor thread
3. "RUNNING" indicator correctly reflects code running in executor
4. internally the ScriptRunContext object is context-managed and won't be leaked
""")
st.session_state["foo"] = "foo-value"

sleep1 = st.number_input("sleep in thread 1", min_value=0, value=1, max_value=6)
dest1 = st.empty()

sleep2 = st.number_input("sleep in thread 2", min_value=0, value=1, max_value=5)
dest2 = st.empty()

timeline_placeholder = st.empty()


update_widget_clicked = st.button(f"Run tasks in executor")


@wrap_sync(with_script_run_context=True)
def time_consuming_task(dest, delay: float):
    start = datetime.datetime.now()
    time.sleep(delay)
    value_from_session_state = st.session_state.get("foo", None)
    dest.markdown(f"""
Widget updated from thread {threading.current_thread().name}, with value in session state: {value_from_session_state}""")
    return (start, datetime.datetime.now())


demo.render_page_src(__file__)


async def main():
    if update_widget_clicked:
        (start1, end1), (start2, end2) = await asyncio.gather(
            time_consuming_task(dest1, sleep1), time_consuming_task(dest2, sleep2)
        )

        timeline_placeholder.markdown(
            f"""
            Concurrent task 1: start={start1} end={end1}

            Concurrent task 2: start={start2} end={end2}

            Script run: end at {datetime.datetime.now()}
            """
        )


asyncio.run(main())
