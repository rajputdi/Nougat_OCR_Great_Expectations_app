import streamlit as st
from modules import Uploader, data_processor, data_validator as dv, data_exporter
import great_expectations as ge

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
            validation_results = dv.validate_dataframe(df)
            ge_df = ge.from_pandas(df)

        # Display the validation results or take some action based on them
        if validation_results["success"]:
            st.write("Dataframe validation passed!")
        else:
            st.write("Dataframe validation failed!")

            st.write(validation_results, "/n")

        config = ge_df.get_expectations_config()

        # Convert the config to an HTML string
        html_content = data_exporter.convert_config_to_html(config)

        # Generate a download link and display it in Streamlit
        download_link = data_exporter.generate_download_link(html_content)
        st.markdown(download_link, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
