# entrypoint of multipage demo app
import streamlit as st
import streamlit_concurrency.demo as scd  # this also inits root logger

# this file may be evalutated in multiple threads.
# wrapping in __name__ help to prevent streamlit warnings in worker process.
# a non workaroundable behavior in multiprocessing ('_fixup_main_from_path')
if __name__ == "__main__":
    st.set_page_config(page_title="streamlit-concurrency")

    st.balloons()

    st.markdown(scd.read_repo_file("README.md"))
