import streamlit as st

def show(df):
    st.dataframe(df, use_container_width=True)
