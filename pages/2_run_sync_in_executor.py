import streamlit as st
import threading
import time
import logging
import asyncio
import streamlit_concurrency as stc
import streamlit_concurrency.demo as stc_demo

SESSION_STATE_KEY = f"{__file__} / session_state"

st.session_state[SESSION_STATE_KEY] = st.number_input("Set session state", value=0)

run = st.button("Run")

result_placeholder = st.container()
log_placeholder = st.empty()


@stc.run_in_executor(with_script_run_context=True)
def read_session_state_and_update_widget():
    value = st.session_state.get(SESSION_STATE_KEY, 0)

    result_placeholder.code(
        f"""
{read_session_state_and_update_widget.__name__} running in thread {threading.current_thread().name}
session_state is {value}
Widget updated by {read_session_state_and_update_widget.__name__}
"""
    )
    time.sleep(2)
    result_placeholder.code(
        f"{read_session_state_and_update_widget.__name__} finished in thread {threading.current_thread().name}"
    )


async def main():
    log_placeholder.code("capturing logs...")
    with stc_demo.create_log_record_sink(logging.DEBUG) as (records, lines):
        if run:
            await read_session_state_and_update_widget()
    log_placeholder.code(
        "\n".join(["logs captured during page run", ""] + lines), wrap_lines=True
    )


stc_demo.render_page_src(__file__)

if __name__ == "__main__" and run:
    asyncio.run(main())
