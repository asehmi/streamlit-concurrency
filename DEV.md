## WANTEDs

## NOTE: function transformer

### Possible inputs

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

### Function transformers

1. run sync function in worker thread AND pass ScriptContext
2. run sync function in worker thread AND get an Awaitable to not block as

## WANT: lifetime signals

1. `PageRunSignal` a signal variable to capture 'page is running'
1. `SessionSignal` a signal variable to capture 'page is running'

## concepts

### `concurrent.future`

`cf.Task`

### `asyncio`

`asyncio`
