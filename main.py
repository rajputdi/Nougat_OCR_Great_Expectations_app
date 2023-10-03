import streamlit as st
from modules import Uploader, data_processor, data_validator


def display_validation_results(df):
    validation_results = data_validator.set_or_update_expectations(df)

    # Extracting statistics from the validation results for display
    for batch in validation_results["results"]:
        batch_name = batch.batch_identifier["batch_identifier"]
        expectation_results = (
            batch.expectation_suite_validation_result.expectation_results
        )

        # Display the results in Streamlit
        st.write(f"## Validation Results for {batch_name}")
        for expectation_result in expectation_results:
            st.write(expectation_result.expectation_config.expectation_type)
            st.write("Success:", expectation_result.success)
            if not expectation_result.success:
                st.write("Details:", expectation_result.result)


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))

        # Validate the data and display the results
        if st.button("Validate Data"):
            display_validation_results(df)


if __name__ == "__main__":
    main()
