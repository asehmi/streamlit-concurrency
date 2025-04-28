# entrypoint of multipage demo app
import streamlit as st
import streamlit_concurrency.demo as scd  # this also inits root logger


st.set_page_config(page_title="streamlit-concurrency")

st.balloons()

st.markdown(scd.read_repo_file("README.md"))
