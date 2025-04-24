import asyncio
import streamlit as st
from streamlit_concurrency import run_in_executor


# streamlit.runtime.caching.cache_errors.UnserializableReturnValueError
@st.cache_data
async def async_function():
    await asyncio.sleep(1)
    return "Async function result"


@run_in_executor()
async def async_function2():
    await asyncio.sleep(1)
    return "Async function result"


clicked = st.button("Click me to run async function")


async def main():
    if clicked:
        result = await async_function2()
        st.write(result)
    else:
        st.write("Click the button to run the async function.")


asyncio.run(main())
