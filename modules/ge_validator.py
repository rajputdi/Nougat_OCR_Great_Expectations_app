import great_expectations as ge
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.data_context.data_context import DataContext

context = DataContext("gx")


def run_checkpoint_on_df(df, context):
    # Convert pandas dataframe to GE dataset
    ge_df = ge.dataset.PandasDataset(df)

    # Run the checkpoint
    results = context.run_checkpoint(
        checkpoint_name="fm_checkpoint_v1", batch_request={"batch_data": ge_df}
    )
    return results
