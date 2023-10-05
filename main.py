import streamlit as st
from modules import Uploader, data_processor, ge_validator as gv
from ydata_profiling import ProfileReport
import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.data_context.data_context import DataContext
import yaml
from great_expectations.checkpoint import Checkpoint


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

            # Add the checkpoint to the DataContext
            context.add_checkpoint(**checkpoint_config)

            # To verify

            available_checkpoints = context.list_checkpoints()
            st.write(available_checkpoints)

            retrieved_checkpoint = context.get_checkpoint(name="fm_checkpoint_v1")
            st.write(retrieved_checkpoint)

            # ge_df = ge.dataset.PandasDataset(df)
            # results = context.run_checkpoint(
            #    checkpoint_name="fm_checkpoint_v1", batch_request={"batch_data": ge_df}
            # )
            # st.write(results)

            results = retrieved_checkpoint.run(
                batch_request={
                    "batch_data": ge_df,
                    "datasource_name": "my_pandas_datasource1",
                    "data_asset_name": "fm_dataframe",
                    "expectation_suite_name": "freddie_mac_expectation_suite",
                }
            )


if __name__ == "__main__":
    main()
