import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
# `run_in_executor` decorator

`run_in_executor` is a decorator to transform functions and run them concurrently.

## Usage

```py
import streamit as st
from streamlit_concurrency import run_in_executor
import asyncio

# transform sync or async function with it
# both sync or async function gets transformed into async function
@run_in_executor(
    cache={'ttl': 1},
    with_script_run_context=True)
def my_sync_func():
    return 'from_sync_func'

@run_in_executor(
    cache={'ttl': 1},
    with_script_run_context=False)
async def my_async_func():
    return 'from_async_func'


# now they can run concurrently
async def page_main():
    ret1, ret2 = await asyncio.gather(
        await my_sync_func()
        await my_async_func()
    )
    st.write((ret1, ret2))

asyncio.run(page_main())
```

## Params

- `cache`: a dict of params to [`st.cache_data`](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data). Defaults to `None` for no cache.
    - Internally it does use `st.cache_data`. All its params except `show_spinner` are supported.
- `with_script_run_context`: When true, pass ScriptRunContext to executor and enable use streamlit APIs from other thread. Defaults to `False`.
    - When this is enabled, the transformed function must be called from a thread containing a ScriptRunContext (typically the thread running a page)
    - See [multithreading](https://docs.streamlit.io/develop/concepts/design/multithreading) for more details about `ScriptRunContext`.

""")

st.markdown(
    """
## Running example

See `run_in_executor example` page for a complete running example
"""
)

st.page_link("pages/4_run_in_executor_example.py", label="`run_in_executor` example")
