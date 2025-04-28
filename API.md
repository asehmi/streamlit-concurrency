# `run_in_executor`

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

Internally `st.cache_data` tries to cache updates to widgets. This may cause problem 

### `cache.show_spinner` is not supported

Not supporting it is simpler. When transformed functions are `await`ed the running indicator works anyway.

# `use_state`

State management util for streamlit pages.

Inspired by [React hook](https://react.dev/reference/react/hooks) and Redux.

## Usage

```py
# `use_state` creates StateRef, a reference to value in st.session_state.
# The value is kept inside st.session_state, keyed with (namespace, key) tuple
page_scoped_state = use_state("page_scoped_ref", namespace=__file__)
session_scoped_state = use_state("page_scoped_ref") # default: namespace=None

# simple reads / writes
s.value = 1
s.value # => 1

# typing & initialization:
#
# type is infered from `factory` callable or `type_`
s = use_state(..., factory=int) # initialize 0
s = use_state(..., type_=int) # not initialized (reading an uninitialized state throws KeyError)

# mutate state with a reducer:
# 
# s.reduce(reducer, *args, **kwargs)
# is the same as
# s.value = reducer(s.value, *args, **kwargs)
s.value = 2
s.reduce(lambda prev, delta: prev + delta, 3)
assert s.value == 5


# clear: or uninitialize a state
s.clear()
```