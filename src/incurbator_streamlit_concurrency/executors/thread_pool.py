from concurrent.futures import ThreadPoolExecutor

sfc_thread_pool_executor = ThreadPoolExecutor(
    thread_name_prefix="streamlit-concurrency-"
)
