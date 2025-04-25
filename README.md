# streamlit-concurrency

Easier and safer concurrency for streamlit.

This library provide APIs:

- `run_in_executor`: transform function to run concurrently in executor (ThreadPoolExecutor)
    - with configurable caching like `st.cache_data`, even for async function
    - transformed function can use `st.session_state` and widget APIs even in other threads
- `use_state`: manage page state in and across pages

## `run_in_executor`: transform sync or async function to run in executor

See [docs/api_run_in_executor.md](docs/api_run_in_executor.md) for details.

## `use_state`: page- or session- scoped state

See [docs/api_run_in_executor.md](docs/api_run_in_executor.md) for details.



## License

Apache 2.0