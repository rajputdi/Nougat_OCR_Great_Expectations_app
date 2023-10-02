import streamlit as st


def file_uploader():
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv"])

    # Check the file type after upload
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1]

        if file_type not in ["txt", "csv"]:
            st.error("Invalid file type. Please upload a .txt or .csv file.")
            return None
        else:
            st.write("Successfully uploaded the file!")
            return uploaded_file

    return None
