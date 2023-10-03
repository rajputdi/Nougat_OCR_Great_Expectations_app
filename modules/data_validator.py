import great_expectations as ge


def set_or_update_expectations(df):
    context = ge.data_context.DataContext()
    suite_name = "loan_data_expectations"
    suite = context.create_expectation_suite(suite_name, overwrite_existing=True)
    ge_df = ge.from_pandas(df)
    batch = ge.dataset.Batch(data=ge_df, batch_request=None, expectation_suite=suite)

    # Example expectation: Credit Score between 300 and 850
    batch.expect_column_values_to_be_between("Credit Score", 300, 850, mostly=0.95)

    # ... add other expectations as necessary ...

    # Save the updated suite
    context.save_expectation_suite(batch.get_expectation_suite(), suite_name)

    # Validate the batch against the suite
    validation_results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[batch]
    )
    return validation_results
