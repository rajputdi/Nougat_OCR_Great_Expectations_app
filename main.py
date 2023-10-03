import streamlit as st
from modules import (
    Uploader,
    report_selector,
    data_processor,
    data_validator,
    data_corrector,
)


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()
    report_choice = report_selector.select_report_type()

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_choice)

        # Generate and display profiling report
        html_report = data_validator.generate_profiling_report(df)
        st.markdown(html_report, unsafe_allow_html=True)

        # Add a button to preview the corrected data
        if st.button("View Data"):
            st.dataframe(df.head(50))  # Display top 50 rows upon button click


if __name__ == "__main__":
    main()
