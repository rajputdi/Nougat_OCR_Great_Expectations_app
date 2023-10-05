import streamlit as st
from modules import Uploader, data_processor, data_validator as dv, data_exporter
import great_expectations as ge
from modules import ge_validator as gv

# ... other imports ...


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
            with st.spinner("Generating report..."):
                report = data_processor.generate_profiling_report(df)
            html = report.to_html()
            st.success("Report generated!")

            st.download_button(
                label="Download Data Summary Report",
                data=html.encode("utf-8"),
                file_name="data_summary.html",
                mime="text/html",
            )

        # -->changes for great expectations
        if st.button("Validate Using GE"):
            # Validate the dataframe using Great Expectations
            validation_results, expectation_result = dv.validate_dataframe(df)
            ge_df = ge.from_pandas(df)

        if validation_results["success"]:
            st.write("Dataframe validation passed!")
            st.write(expectation_result, "\n")
        else:
            st.write("Dataframe validation failed!")
            st.write(expectation_result, "\n")
        # st.write(validation_results, "/n")
        # st.write(expectation_result, "/n")

        # Validate the dataframe using GE and display results
        if st.button("Validate Data"):
            results = gv.validate_dataframe(df)
            st.write(results)


if __name__ == "__main__":
    main()
