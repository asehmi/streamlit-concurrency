import streamlit as st
import threading
import logging
import asyncio
import streamlit_concurrency as stc
import streamlit_concurrency.demo as stc_demo

logger = logging.getLogger(__name__)
st.set_page_config(layout="wide")

col1, col2 = st.columns(2, vertical_alignment="bottom")
with col1:
    input_to_cached_function = st.number_input(
        "Argument to cached async function", value=0, min_value=0, max_value=10
    )
with col2:
    run = st.button("Run")

progress_placeholder = st.empty()
progress_placeholder.markdown(
    "*Placeholder* progress from within cached async function"
)

log_placeholder = st.empty()
log_placeholder.markdown("*Placeholder* logs captured during runs")


res_placeholder = st.empty()


@stc.run_in_executor(
    with_script_run_context=True,
    cache={"ttl": 10, "max_entries": 3},
)
async def cached_async(input: int):
    await asyncio.sleep(2)
    log1 = f"""{cached_async.__name__}(input={input}) running in thread {threading.current_thread().name}"""
    logger.info("log1 %s", log1)
    progress_placeholder.code(log1)
    await asyncio.sleep(2)

    log2 = f"{cached_async.__name__}(input={input}) finished in thread {threading.current_thread().name}"
    progress_placeholder.code("\n".join([log1, log2]))
    logger.info("log2 %s", log2)
    return input


async def main():
    # log_placeholder.code("capturing logs...")
    if run:
        throttled_res, _ = await asyncio.gather(
            cached_async(input_to_cached_function),
            stc_demo.capture_logs_render_df(
                log_placeholder, duration=4, level=logging.DEBUG
            ),
        )
        res_placeholder.code(
            f"@run_in_executor(cache=...) {cached_async.__name__}(input={input_to_cached_function}) returned {throttled_res}"
        )


stc_demo.render_page_src(__file__)

if __name__ == "__main__":
    asyncio.run(main())
