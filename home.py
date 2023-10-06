import streamlit as st
from pages.main import main
from pages.diagram import diagram


def home():
    st.title("DAMG 7245 - Assignment 01-Part 2")


page_names_to_funcs = {
    "Home": home,
    "Streamlit App": main,
    "Architecture": diagram,
}

# Reset the sidebar to ensure no stray content
st.sidebar.empty()

# Sidebar Navigation
demo_name = st.sidebar.selectbox("Choose an option", list(page_names_to_funcs.keys()))
st.sidebar.success("Select from the dropdown above☝")

# Content of selected page
page_names_to_funcs[demo_name]()
