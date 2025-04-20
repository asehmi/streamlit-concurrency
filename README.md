# streamlit-concurrency

The library for simpler and safer concurrency in streamlit.

Based on [how threads work in streamlit](https://docs.streamlit.io/develop/concepts/design/multithreading), this library provides opinionated helpers to

- transform slow functions to run in `concurrent.future.Executor` (ThreadPoolExecutor, ProcessPoolExecutor and more)
- access streamlit APIs like `st.write` and `st.session_state` in different threads
- minimize user's wait time

<!-- TODO future
- simplify state management in and across pages
- listen for cancelled page run or terminated session, and prevent unnecessary code run
-->

## Recommended 


## Example pages

- `incorrect_multithreading`: what happens when 
- `function decorators`: executor / caching / `st.
- `

## Concurrency function decorators

## State management

## Page run or session lifetime signals


## Possible inputs

1. streamlit code
    - sync & can work in any thread
    - sync & expects a ScriptThread
    - (AFAIK streamlit has no async API)
2. user code, including libs
    - sync
        - CPU intensive -> worker? (maybe process worker)
        - IO wait -> run in worker thread, reape as `cf.Future` or `Awaitable`
    - async
        - CPU intensive -> run in a different loop won't help
        - IO wait: not a problem

## Function transformers

1. run sync function in worker thread AND pass ScriptContext
2. run sync function in worker thread AND get an Awaitable to not block as


## utils

1. `PageRunSignal` a signal variable to capture 'page is running'
1. `SessionSignal` a signal variable to capture 'page is running'

## concepts

### `concurrent.future`

`cf.Task`

### `asyncio`

`asyncio`

3. await on 
    - `asyncio.gather`: start and 
    - `asyncio.TaskGroup`: auto cancelling