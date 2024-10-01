import streamlit as st
import time
from threading import Thread


class WorkerThread(Thread):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.return_value = None

    def run(self):
        # runs in custom thread, touches no Streamlit APIs
        start_time = time.time()
        time.sleep(self.delay)
        end_time = time.time()
        self.return_value = f"start: {start_time}, end: {end_time}"


st.header("t1")
result_1 = st.empty()
st.header("t2")
result_2 = st.empty()


def main():
    t1 = WorkerThread(5)
    t2 = WorkerThread(5)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # main() runs in script thread, and can safely call Streamlit APIs
    result_1.write(t1.return_value)
    result_2.write(t2.return_value)


main()
