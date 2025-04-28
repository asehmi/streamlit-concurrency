import streamlit as st
import threading
import time
import asyncio
import datetime
import streamlit_concurrency.demo as demo
from streamlit_concurrency import run_in_executor

logger = demo.logger

st.markdown("""
This page demostrates multithreading with `streamlit-concurrency`.
            
Compared to `troubled multithreading` example:

1. widget can be updated from another thread
2. session state can be accessed in another thread
3. "RUNNING" indicator correctly reflects code running in executor
4. internally the ScriptRunContext object gets context-managed and won't be leaked

""")
st.session_state["foo"] = "foo-value"

col1, col2 = st.columns(2)
with col1:
    sleep1 = st.number_input("Task 1 duration", min_value=0, value=1, max_value=5)
    dest1 = st.container()

with col2:
    sleep2 = st.number_input("Task 2 duration", min_value=0, value=2, max_value=5)
    dest2 = st.container()

timeline_placeholder = st.empty()


update_widget_clicked = st.button(f"Run 2 tasks concurrently in executor")


@run_in_executor(with_script_run_context=True)
def time_consuming_task(dest, duration: float, interval=0.2):
    start = datetime.datetime.now()
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    value_from_session_state = st.session_state.get("foo", None)
    dest.write(f"st.session_state['foo'] is {value_from_session_state}")
    while datetime.datetime.now() < deadline:
        dest.markdown(
            f"""{datetime.datetime.now()} running in thread `{threading.current_thread().name}`"""
        )
        time.sleep(interval)
    return (start, datetime.datetime.now())


demo.render_page_src(__file__)


async def main():
    if update_widget_clicked:
        (start1, end1), (start2, end2) = await asyncio.gather(
            time_consuming_task(dest1, sleep1), time_consuming_task(dest2, sleep2)
        )

        timeline_placeholder.markdown(
            f"""
---

Task 1: start={start1} end={end1}

Task 2: start={start2} end={end2}

Script run finishes at {datetime.datetime.now()}
""".strip()
        )


asyncio.run(main())
