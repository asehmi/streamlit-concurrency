import datetime
import time
import asyncio
import streamlit as st
import threading
import logging

from streamlit_concurrency import run_in_executor
import streamlit_concurrency.demo as stc_demo

logger = logging.getLogger(__name__)

col1, col2 = st.columns(2)
with col1:
    st.session_state["_value"] = st.number_input(
        "set session_state['_value']:", value=0
    )
with col2:
    param_value = st.number_input("set param:", value=0)

run_clicked = st.button("Run")


@run_in_executor(cache={"ttl": 3})
def sync_function(param: int):
    logger.info("sync_function got param=%d", param)
    return datetime.datetime.now()


@run_in_executor(with_script_run_context=True)
async def run_sync_function(param):
    session_state_value = st.session_state.get("_value", None)
    sync_function_res = await sync_function(param)
    widget_for_sync.markdown(f"""
{sync_function.__name__} returned {sync_function_res}

`param`: {param}

`session_state['_value']`: {session_state_value}

time: {datetime.datetime.now()}""")


@run_in_executor(cache={"ttl": 3}, with_script_run_context=True)
async def async_function(param: int):
    await asyncio.sleep(0.2)
    logger.info("sync_function got param=%d", param)
    session_state_value = st.session_state.get("_value", None)
    widget_for_async.markdown(f"""
Widget updated by {async_function.__name__} running in {threading.current_thread().name}

`param`: {param}

`session_state['_value']`: {session_state_value}

time: {datetime.datetime.now()}""")
    return datetime.datetime.now()


col1, col2, col3 = st.columns(3, border=True)
with col1:
    widget_for_sync = st.empty()

with col2:
    widget_for_async = st.empty()

with col3:
    widget_for_main = st.empty()


st.write("captured logs")
logging_dest = st.empty()


async def main():
    sync_result, async_result, _ = await asyncio.gather(
        sync_function(param_value),
        async_function(param_value),
        stc_demo.capture_logs_render_df(
            logging_dest,
            duration=3,
            update_interval=0.1,
        ),
    )
    widget_for_main.markdown(f"""
`sync_function()` returned `{sync_result}`

`async_function()` returned `{async_result}`

main() running in {threading.current_thread().name}
    """)


stc_demo.render_page_src(__file__)

if __name__ == "__main__" and run_clicked:
    asyncio.run(main())
