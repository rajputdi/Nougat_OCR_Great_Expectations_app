import streamlit as st
from pages.main import main
from pages.diagram import diagram


def home():
    st.title("DAMG 7245 - Assignment 01-Part 2")


st.write(
    """
Your team is tasked with building a tool to use the Freddie mac single family dataset [1]. You in the data
engineering group are asked to build a tool so you can evaluate the quality of the dataset and if it adheres to
the schema [2] that is published.

- Your tool will be built using streamlit
- A user would upload a csv/xls file and indicate if it is Origination/Monthly performance data
- You should use pandasprofiling to summarize the data and display to the end user
- You should run greatexpectations to ensure:
    * The data schema is correct
    * The data is valid
    * There is no missing data
    * Any other tests you can think of (2-5)
- Create and embed the architecture of the project using diagrams[6] within Streamlit
         
-Submission by: Team 4 
         * Divyesh Rajput
         * Naman Gupta
         * Jagruti Agrawal
"""
)


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
