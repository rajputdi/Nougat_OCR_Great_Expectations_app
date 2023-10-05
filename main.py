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
            # Generate the report
            report = ProfileReport(
                df, title="Data Summary using ydata-profiling", minimal=True
            )
        if st.button("Run Checkpoint"):
            context = DataContext("gx")
            st.write(context)
            with open("gx/checkpoints/fm_checkpoint_v1.yml", "r") as stream:
                checkpoint_config = yaml.safe_load(stream)
            with open(
                "gx/expectations/freddie_mac_expectation_suite.json", "r"
            ) as file:
                suite_data = json.load(file)

            # Convert the dictionary to an ExpectationSuite
            suite = ExpectationSuite(suite_data)

            # Add the suite to the context
            context.save_expectation_suite(suite, "freddie_mac_expectation_suite")

            # Add the checkpoint to the DataContext
            context.add_checkpoint(**checkpoint_config)
            context.add_expectation_suite()
            # To verify

            available_checkpoints = context.list_checkpoints()
            st.write(available_checkpoints)

            available_suites = context.list_expectation_suites()
            st.write(available_suites)

            retrieved_checkpoint = context.get_checkpoint(name="fm_checkpoint_v1")
            st.write(retrieved_checkpoint)

            # suite = context.get_expectation_suite("freddie_mac_expectation_suite")
            # results = ge_df.validate(expectation_suite=suite)

            # ge_df = ge.dataset.PandasDataset(df)
            # results = context.run_checkpoint(
            #     checkpoint_name="fm_checkpoint_v1",
            #     batch_request={
            #         "batch_data": ge_df,
            #         "datasource_name": "my_pandas_datasource1",
            #         "data_asset_name": "fm_dataframe",
            #     },
            # )
            st.write(results)


if __name__ == "__main__":
    main()
