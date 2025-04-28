import streamlit as st
import pandas as pd

st.write("write text")

st.dataframe(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))

int_value = st.number_input("Enter an integer", value=0)

st.write("You entered:", int_value)
