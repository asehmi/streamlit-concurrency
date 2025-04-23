"""Reproduction for "altering clsoure-capured variable" case in https://github.com/streamlit/streamlit/issues/11157"""

import streamlit as st

free_variable = 0


def uncached(param: int):
    return f"free_variable={free_variable} param={param}"


cached = st.cache_data(uncached)


param_value = st.number_input("param", value=0, step=1)

run = st.button(f"alter free_variable to {param_value} and call")

if run:
    free_variable = param_value
    st.write(f"uncached({1}) things {uncached(1)}")
    st.write(f"cached({1}) thinks {cached(1)}")
