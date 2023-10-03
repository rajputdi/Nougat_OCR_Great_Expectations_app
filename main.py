import streamlit as st
from modules import Uploader, report_selector, data_processor, data_validator


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()
    report_choice = report_selector.select_report_type()

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_choice)

        # Initialize and set expectations before generating the report
        suite = data_validator.initialize_expectations()
        data_validator.set_credit_score_expectation(suite)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))

        # Generate and display the GE profiling report if the respective button is clicked
        if st.button("View GE Profiling Report"):
            html_report = data_validator.generate_profiling_report(df)
            st.markdown(html_report, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
