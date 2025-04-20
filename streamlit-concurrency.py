# entrypoint of multipage demo app
import streamlit as st
import streamlit_concurrency.demo as scd

st.set_page_config(page_title="streamlit-concurrency")

st.markdown(scd.read_repo_file("README.md"))
