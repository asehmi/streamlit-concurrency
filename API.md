# `run_in_executor`

`run_in_executor` transforms functions to run them concurrently.

## Usage

```py
import streamit as st
from streamlit_concurrency import run_in_executor
import asyncio

# the simplest way to use is to decoreate a function (only works for 'thread' executor)
# both sync or async function are supported, and both get transformed into async function
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

# a function to run in non-thread executor cannot use the decorator syntax
# (it has to have a separate importable definition)
from streamlit_concurrency.demo import example_func
remote_sync_func = run_in_executor(executor="process", cache={"ttl": 5})(
    example_func.cpu_intensive_computation
)

# now they can run concurrently inside script thread
async def page_main():
    ret1, ret2, ret3 = await asyncio.gather(
        await my_sync_func()
        await my_async_func()
        await remote_sync_func()
    )
    st.write((ret1, ret2, ret3))

asyncio.run(page_main())
```

### Param: `cache: dict | None = None`

`cache` accepts a dict of params identical to [`st.cache_data`](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data).

- Internally it does use `st.cache_data`. All `st.cache_data` params except `show_spinner` are supported.


### Param: `with_script_run_context: bool = False`

When true, capture the ScriptRunContext and add it to the executor thread running . Defaults to `False`.

- See [streamlit / multithreading](https://docs.streamlit.io/develop/concepts/design/multithreading) for more details about `ScriptRunContext`.

- Enable this when you need to use streamlit APIs (`st.session_state` or widgets) from other thread

- When this is enabled, the transformed function must be called from a thread containing a ScriptRunContext (typically a thread running page code)

## Param: `executor: 'thread' | 'process' = 'thread'`


### About `process` executor

There are certain limits for a function to run in a _process_ executor, which is based on `concurrency.future.ProcessPoolExecutor`:

0. The function cannot be `async`.

1. The original function must be _importable_, or defined at the top level of a importable module.
    - This means `run_in_executor` cannot be used as a decorator.
    - This also means the function has to be defined in a separate non-page module.

2. The function should not depend on any Streamlit code. This includes other functions transformed by `run_in_executor` or `st.cache_*`.

3. The arguments and return value of the function need to pickle-serializable.

The recommended use is to define a self-contained worker entrypoint in separate module, handling required initialization. And transform it in page like `run_in_executor(executor='process')(entrypoint)`

`cache=` still works. It is handled in stremalit process and can still cache the result value from executor process.

`multiprocessing` has a non-configurable behavior to load the entry script (the one specified in `streamlit run`) in worker process. This may cause warnings like `missing ScriptRunContext` or `to view a Streamlit app on a browser...`. If no worse error occurs the warnings can be ignored. You can try to remove such warnings or errors like:

```py
# root_page.py
import streamlit as st

if __name__ == '__main__':
    # this does not get executed in worker process
    st.markdown(...)


```


## Recommended programming style: structured concurrency

<!-- TODO: more -->

<!-- TBD: should we recommend more complete framework like trio?-->

## Caveats & FAQ



### `cache` and `with_script_run_context` together may cause problem

In some versions of Streamlit it tries to cache widget updates from a function inside `st.cache_data()`. If you used both and see strange errors, try removing 1.

### `cache.show_spinner` is not supported

<!--
Supporting it would implicitly (showing a spinner requires a ScriptRunContext)
-->

Not supporting it is simpler. When transformed functions are `await`ed in the script thread, the running human indicator works anyway.

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