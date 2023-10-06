import streamlit as st
from modules import Uploader, data_processor, ge_validator as gv
from ydata_profiling import ProfileReport
import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.data_context.data_context import DataContext
import yaml
from great_expectations.checkpoint import Checkpoint
import json
from great_expectations.core.expectation_suite import ExpectationSuite
import requests
import html


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    report_type = st.radio(
        "Choose type of report", ["Origination Report", "Monthly Performance Report"]
    )

    link_label = "Want to know more about the dataset? Click me!"
    link_url = "https://www.freddiemac.com/fmac-resources/research/pdf/user_guide.pdf"
    st.markdown(f"[{link_label}]({link_url})")

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_type)

        ge_df = ge.from_pandas(df)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))

        if st.button("Generate Data Summary"):
            with st.spinner("Generating report..."):
                report = data_processor.generate_profiling_report(df, report_type)
            html1 = report.to_html()
            st.success("Report generated!")

            st.download_button(
                label="Download Data Summary Report",
                data=html1.encode("utf-8"),
                file_name="data_summary.html",
                mime="text/html",
            )

        if st.button("Run Validations using Expectation Suite"):
            if report_type == "Origination Report":
                GITHUB_RAW_URL = "https://raw.githubusercontent.com/rajputdi/test_repo/main/gx/expectations/freddie_mac_expectation_suite1.json"
            else:  # monthly performance expectation suite
                GITHUB_RAW_URL = "https://raw.githubusercontent.com/rajputdi/test_repo/main/gx/expectations/freddie_mac_expectation_suiteMP.json"
            response = requests.get(GITHUB_RAW_URL)
            if response.status_code == 200:
                expectation_suite = response.json()
            else:
                raise ValueError("Failed to fetch the expectation suite from GitHub.")

            # Convert the dictionary back to an ExpectationSuite object
            suite_obj = ExpectationSuite(**expectation_suite)
            # Now, set this suite to your ge_df
            ge_df._expectation_suite = suite_obj
            results = ge_df.validate()

            pretty_json_str = json.dumps(results.to_json_dict(), indent=4)

            # Embed the JSON in an HTML template.
            html_content = f"""
            <html>
            <head>
            <title>Validation Results</title>
            </head>
            <body>
            <pre>{pretty_json_str}</pre>
            </body>
            </html>
            """

            # Convert the HTML content to bytes.
            b_content = bytes(html_content, "utf-8")

            # Streamlit button for download.
            st.download_button(
                "Download Validation Result",
                b_content,
                file_name="results.html",
                mime="text/html",
            )
