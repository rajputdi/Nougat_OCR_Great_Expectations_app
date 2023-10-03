import streamlit as st
from modules import uploader, report_selector, data_processor


def main():
    st.title("Streamlit App")

    st.write("Upload a file for this session:")
    uploaded_file = uploader.file_uploader()

    report_choice = report_selector.select_report_type()

    # Process and display the data
    if uploaded_file:
        df = data_processor.process_txt(uploaded_file)
        st.dataframe(df.head(50))  # Display top 50 rows


if __name__ == "__main__":
    main()
