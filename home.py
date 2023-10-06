import streamlit as st
from pages.main import main
from pages.diagram import diagram

page_names_to_funcs = {
    "Home": lambda: st.title("DAMG 7245 - Assignment 01-Part 2-Team 4"),
    "Streamlit App": main,
    "Architecture": diagram,
}

# Ensure the sidebar-specific calls are made first
demo_name = st.sidebar.selectbox("Choose an option", list(page_names_to_funcs.keys()))
st.sidebar.success("Select from the dropdown above☝")

# Then call the main page function
page_names_to_funcs[demo_name]()
