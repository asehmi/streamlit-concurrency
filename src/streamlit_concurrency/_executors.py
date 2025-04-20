import functools
import concurrent.futures as cf

# TODO this should be lazy inited
# TODO initialization should be mutex-protected


@functools.lru_cache(maxsize=1)
def _get_thread_pool_executor() -> cf.Executor:
    return cf.ThreadPoolExecutor(thread_name_prefix="streamlit-concurrency-")


@functools.lru_cache(maxsize=1)
def _get_process_pool_executor() -> cf.Executor:
    return cf.ProcessPoolExecutor()


@functools.lru_cache(maxsize=1)
def _get_interpreter_pool_executor() -> cf.Executor:
    # should be available since py3.14
    return cf.InterpreterPoolExecutor()
