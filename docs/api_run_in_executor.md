# `run_in_executor` decorator

`run_in_executor` decorator transforms functions to run them concurrently.

## Usage

```py
import streamit as st
from streamlit_concurrency import run_in_executor
import asyncio

# both sync or async function are supported, and get transformed into async function
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

## Param: `cache: dict | None = None`

`cache` accepts a dict of params identical to [`st.cache_data`](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data).

- Internally it does use `st.cache_data`. All `st.cache_data` params except `show_spinner` are supported.


## Param: `with_script_run_context: bool = False`

When true, capture the ScriptRunContext and add it to the executor thread running . Defaults to `False`.

- See [streamlit / multithreading](https://docs.streamlit.io/develop/concepts/design/multithreading) for more details about `ScriptRunContext`.

- Enable this when you need to use streamlit APIs (`st.session_state` or widgets) from other thread

- When this is enabled, the transformed function must be called from a thread containing a ScriptRunContext (typically a thread running page code)

## Caveats

### Better not enable `cache` and `with_script_run_context` together

Internally `st.cache_data` tries . This may cause problem 

### `cache.show_spinner` is not supported

This is due to 
- `Rreplay`
    - 
Using both on 1 
Is possible yet unrecommended.
This is due 

To workaround this 
