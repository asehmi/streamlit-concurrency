from concurrent.futures import ThreadPoolExecutor

# TODO this should be lazy inited
# TODO initialization should be mutex-protected

sfc_thread_pool_executor = ThreadPoolExecutor(
    thread_name_prefix="streamlit-concurrency-"
)
