import great_expectations as ge


def initialize_expectations():
    context = ge.data_context.DataContext()
    suite = context.create_expectation_suite("loan_data_expectations")
    context.save_expectation_suite(suite)
    return suite


def set_credit_score_expectation(suite):
    suite.add_expectation(
        {
            "expectation_type": "expect_column_values_to_be_between",
            "kwargs": {"column": "Credit Score", "min_value": 300, "max_value": 850},
        }
    )


def validate_data(df):
    context = ge.data_context.DataContext()
    suite = context.get_expectation_suite("loan_data_expectations")

    # If the suite is empty (first run), initialize expectations
    if not suite.expectations:
        suite = initialize_expectations()
        set_credit_score_expectation(suite)

    ge_df = ge.from_pandas(df)
    results = ge_df.validate(expectation_suite=suite)

    return results
