import streamlit as st
from modules import uploader, report_selector


def main():
    st.title("Streamlit App")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    # Use the report selector module
    report_choice = report_selector.select_report_type()
    if report_choice:
        st.write(f"You selected: {report_choice}")

    # Other functionalities can be added as you specify further requirements.


if __name__ == "__main__":
    main()
