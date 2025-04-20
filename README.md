# streamlit-concurrency

Simpler and safer concurrency for streamlit.

To detail, it

- Run slow or heavy code with `asyncio` or `concurrent.future.Executor`

- State management inside or across pages

- Reduce wait by caching / executor / asyncio

- Save resource by signals
    - Auto stop running when a new page run starts (i.e. a new `ScriptThread`)
    - Auto release when session `SessionContext` stops

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