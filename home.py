import streamlit as st
from pages.main import main
from pages.diagram import diagram


def home():
    st.title("DAMG 7245 - Assignment 01-Part 2-Team 4")
    st.sidebar.success("Select from the dropdown above☝")


page_names_to_funcs = {
    "Home": home,
    "Streamlit App": main,
    "Architecture": diagram,
}

# Place this line at the top, before any other Streamlit calls
demo_name = st.sidebar.selectbox("Choose an option", page_names_to_funcs.keys())
# Invoke the corresponding function
page_names_to_funcs[demo_name]()
