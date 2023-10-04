import streamlit as st
from modules import Uploader, data_processor, data_validator as dv
from ydata_profiling import ProfileReport


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    report_type = st.radio(
        "Choose type of report", ["Origination Report", "Monthly Performance Report"]
    )

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_type)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))
        if st.button("Generate Data Summary"):
            # Generate the report
            report = ProfileReport(
                df, title="Data Summary using ydata-profiling", minimal=True
            )
        if st.button("Validate with Great Expectations"):
            # Initialize Great Expectations context
            context = dv.initialize_ge_context()

            # Set or update expectations
            dv.set_or_update_expectations(context)

            # Validate the data
            batch = context.get_batch(
                {
                    "batch_kwargs": {
                        "datasource": "my_datasource",
                        "dataset": df,
                        "data_asset_name": "uploaded_data",
                    },
                    "expectation_suite_name": "default_suite",
                }
            )
    results = batch.validate()

    # Display validation results
    st.subheader("Validation Results")
    st.write(results)


if __name__ == "__main__":
    main()
