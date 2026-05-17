import streamlit as st

def metric(label: str, value, help_text: str | None = None):
    st.metric(label, value, help=help_text)
