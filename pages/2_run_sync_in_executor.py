import streamlit as st
import threading
import asyncio
import streamlit_concurrency as stc
import streamlit_concurrency.demo as stc_demo

SESSION_STATE_KEY = f"{__file__} / session_state"

st.session_state[SESSION_STATE_KEY] = st.number_input("Set session state", value=0)

run = st.button("Run")

result_placeholder = st.empty()
log_placeholder = st.empty()


@stc.run_in_executor(with_script_run_context=True)
def access_session_state_and_update_widget():
    value = st.session_state.get(SESSION_STATE_KEY, 0)

    result_placeholder.code(
        f"""
value={value}
updated by {access_session_state_and_update_widget.__name__}
from thread {threading.current_thread().name}"""
    )


async def main():
    if run:
        await access_session_state_and_update_widget()


stc_demo.render_page_src(__file__)

if __name__ == "__main__" and run:
    asyncio.run(main())
