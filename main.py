import streamlit as st
from modules import Uploader, report_selector, data_processor


def main():
    st.title("Streamlit App")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    report_choice = report_selector.select_report_type()

    # Process the data
    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_choice)

        # Add a button to preview the data
        if st.button("View Data"):
            st.dataframe(df.head(50))  # Display top 50 rows upon button click


if __name__ == "__main__":
    main()
