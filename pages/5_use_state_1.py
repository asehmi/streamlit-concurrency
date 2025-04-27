import streamlit as st
from streamlit_concurrency import use_state
import streamlit_concurrency.demo as demo

page_scoped_state = use_state("page_scoped_ref", namespace=__file__, type_=int)
page_scoped_state.init(int)

session_scoped_state = use_state("page_scoped_ref", type_=int)
session_scoped_state.init(int)

st.markdown(f"""
This page shows the use of `use_state` to manage state in Streamlit apps.

Switch between this page and `use state 1` to see how they works.

""")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"page_scoped_state.value: `{page_scoped_state.value}`")

    if st.button("Update page-scoped state"):
        page_scoped_state.reduce(lambda prev: prev + 1)
        st.rerun()

    if st.button("Clear page-scoped state"):
        page_scoped_state.clear()
        st.rerun()

with col2:
    st.markdown(f"session_scoped_state.value: `{session_scoped_state.value}`")

    if st.button("Update session-scoped state"):
        session_scoped_state.reduce(lambda prev: prev + 1)
        st.rerun()

    if st.button("Clear session-scoped state"):
        session_scoped_state.clear()
        st.rerun()

demo.render_page_src(__file__)
