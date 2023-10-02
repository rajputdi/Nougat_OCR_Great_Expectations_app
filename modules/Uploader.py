import streamlit as st


def file_uploader():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        st.write("Successfully uploaded the file!")

    return uploaded_file
