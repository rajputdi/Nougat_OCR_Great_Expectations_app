import streamlit as st
from modules import Uploader, data_processor, data_validator


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file)

        # Initialize and set expectations before generating the report
        suite = data_validator.initialize_expectations()
        data_validator.set_credit_score_expectation(suite)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))

        # Generate and display the GE profiling report if the respective button is clicked
        if st.button("View GE Profiling Report"):
            html_url = data_validator.generate_profiling_report(df)
            st.markdown(f"[Click here to view the GE Profiling Report]({html_url})")


if __name__ == "__main__":
    main()
