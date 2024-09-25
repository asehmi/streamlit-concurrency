import streamlit as st
from threading import Thread

dest = st.empty()


@st.cache_data()
def get_data():
    return "dummy"


class BadThread(Thread):
    def run(self):
        data = get_data()
        dest.write(data)


def main():
    t = BadThread()
    t.start()
    t.join()


main()
