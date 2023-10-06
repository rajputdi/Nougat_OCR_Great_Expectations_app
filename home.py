import streamlit as st
from pages.main import main
from pages.diagram import diagram


def home():
    st.title("DAMG 7245 - Assignment 01-Part 2")
    st.sidebar.success("Select from the dropdown above☝")


page_names_to_funcs = {
    "Home": home,
    "Streamlit App": main,
    "Architecture": diagram,
}

# This sidebar logic will run on every page, because it's globally scoped.
demo_name = st.sidebar.selectbox("Choose an option", list(page_names_to_funcs.keys()))

# Content of selected page
page_names_to_funcs[demo_name]()
