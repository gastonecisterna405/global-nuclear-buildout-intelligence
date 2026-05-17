import streamlit as st

def multiselect_filter(label, values):
    vals = sorted([v for v in values if str(v) != "nan"])
    return st.sidebar.multiselect(label, vals, default=vals)
