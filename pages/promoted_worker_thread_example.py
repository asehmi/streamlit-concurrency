import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
import time
from threading import Thread


class WorkerThread(Thread):
    def __init__(self, delay, target):
        super().__init__()
        self.delay = delay
        self.return_value = None
        self.target = target

    def run(self):
        # runs in custom thread, but can call Streamlit APIs
        start_time = time.time()
        time.sleep(self.delay)
        end_time = time.time()
        self.target.write(f"start: {start_time}, end: {end_time}")


st.header("t1")
result_1 = st.empty()
st.header("t2")
result_2 = st.empty()


def main():
    t1 = WorkerThread(5, result_1)
    t2 = WorkerThread(5, result_2)
    # obtain the ScriptRunContext of current Script Thread, and assign to worker threads
    add_script_run_ctx(t1, get_script_run_ctx())
    add_script_run_ctx(t2, get_script_run_ctx())
    t1.start()
    t2.start()
    t1.join()
    t2.join()


main()
