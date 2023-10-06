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
import os
import requests


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    report_type = st.radio(
        "Choose type of report", ["Origination Report", "Monthly Performance Report"]
    )

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_type)

        # Convert the DataFrame to a GE dataset
        ge_df = ge.from_pandas(df)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))

        if st.button("Generate Data Summary"):
            with st.spinner("Generating report..."):
                report = data_processor.generate_profiling_report(df, report_type)
            html = report.to_html()
            st.success("Report generated!")

            st.download_button(
                label="Download Data Summary Report",
                data=html.encode("utf-8"),
                file_name="data_summary.html",
                mime="text/html",
            )

        if st.button("Run Checkpoint"):
            context = DataContext("gx")
            st.write(context)
            # st.write(context.get_expectation_suite("freddie_mac_expectation_suite"))

            # Point directly to the great_expectations.yml within the gx directory
            ge_config_path = "gx/great_expectations.yml"
            context1 = DataContext(ge_config_path)
            st.write(context1)

            # def diagnostic_print_ge_directory(ge_directory_path):
            #     for root, dirs, files in os.walk(ge_directory_path):
            #         for file in files:
            #             print(os.path.join(root, file))

            # diagnostic_print_ge_directory("gx")

        #     # with open("gx/checkpoints/fm_checkpoint_v1.yml", "r") as stream:
        #     #     checkpoint_config = yaml.safe_load(stream)
        #     # context.add_checkpoint(**checkpoint_config)

        #     # with open(
        #     #     "gx/expectations/freddie_mac_expectation_suite.json", "r"
        #     # ) as file:
        #     #     suite_data = json.load(file)

        #     # Convert the dictionary to an ExpectationSuite
        #     suite = ExpectationSuite(suite_data)
        #     st.write(suite)
        #     # Add the checkpoint to the DataContext
        #     # To verify

        #     # Add the suite to the context
        #     context.save_expectation_suite(suite, "freddie_mac_expectation_suite")

        #     ge_df = ge.dataset.PandasDataset(df)

        #     available_checkpoints = context.list_checkpoints()
        #     st.write(available_checkpoints)

        #     available_suites = context.list_expectation_suites()
        #     st.write(available_suites)

        #     retrieved_checkpoint = context.get_checkpoint(name="fm_checkpoint_v1")
        #     st.write(retrieved_checkpoint)

        #     retrieved_suite = context.get_expectation_suite(
        #         "freddie_mac_expectation_suite"
        #     )
        #     st.write(retrieved_suite)

        #     suite = context.get_expectation_suite("freddie_mac_expectation_suite")
        #     st.write(ge_df.head())
        #     results = ge_df.validate(expectation_suite=suite)

        #     url = "https://raw.githubusercontent.com/rajputdi/test_repo/main/gx/expectations/freddie_mac_expectation_suite.json"

        #     response = requests.get(url)
        #     suite_json = response.json()

        #     suite1 = ExpectationSuite(suite_json)
        #     # st.write(suite1)

        #     results_exp = ge_df.validate(expectation_suite=suite1)

        #     # results = context.run_checkpoint(
        #     #     checkpoint_name="fm_checkpoint_v1",
        #     #     batch_request={
        #     #         "batch_data": ge_df,
        #     #         "datasource_name": "my_pandas_datasource1",
        #     #         "data_asset_name": "fm_dataframe",
        #     #     },
        #     # )
        #     st.write(results_exp)

        #     datasource = context.sources.add_pandas(name="my_pandas_datasource2")
        #     name = "fm_dataframe"
        #     data_asset = datasource.add_dataframe_asset(name=name)
        #     my_batch_request = data_asset.build_batch_request(dataframe=df)
        #     checkpoint = context.add_or_update_checkpoint(
        #         name="fm_checkpoint_v1",
        #         validations=[
        #             {
        #                 "batch_request": my_batch_request,
        #                 "expectation_suite_name": "freddie_mac_expectation_suite",
        #             },
        #         ],
        #     )
        #     checkpoint_result = checkpoint.run(run_name="manual_run_1")
        #     st.write(checkpoint_result)

        # #     data_docs_path = "gx/uncommitted/data_docs/local_site/index.html"

        # #     with open(data_docs_path, "r", encoding="utf-8") as file:
        # #         html_content = file.read()

        # #     st.download_button(
        # #         label="Download Data Docs",
        # #         data=html_content,
        # #         file_name="data_docs.html",
        # #         mime="text/html",
        # #     )
        # # else:
        # #     st.write("Data docs have not been generated yet.")


if __name__ == "__main__":
    main()
