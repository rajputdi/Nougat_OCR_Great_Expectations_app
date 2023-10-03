import great_expectations as ge


def initialize_expectations():
    """
    Initialize the expectation suite for the loan data.
    """
    context = ge.data_context.DataContext()

    # Try to get the existing suite. If not, create a new one.
    try:
        suite = context.get_expectation_suite("loan_data_expectations")
    except ge.exceptions.exceptions.DataContextError:
        suite = context.create_expectation_suite("loan_data_expectations")
        context.save_expectation_suite(suite)

    return suite


def set_credit_score_expectation(suite):
    """
    Set the expectation for the Credit Score column.
    """
    expectation_configuration = {
        "expectation_type": "expect_column_values_to_be_between",
        "kwargs": {"column": "Credit Score", "min_value": 300, "max_value": 850},
    }

    # Accessing the dictionary key correctly
    suite.add_expectation(expectation_configuration)


def validate_data(df):
    """
    Validate the dataframe against the defined expectation suite.
    """
    context = ge.data_context.DataContext()
    suite = context.get_expectation_suite("loan_data_expectations")

    # If the suite is empty (first run), initialize expectations
    if not suite.expectations:
        suite = initialize_expectations()
        set_credit_score_expectation(suite)

    ge_df = ge.from_pandas(df)
    results = ge_df.validate(expectation_suite=suite)

    return results


def generate_profiling_report(df):
    """
    Generate a data profiling report for the provided dataframe.
    """
    context = ge.data_context.DataContext()
    suite = context.get_expectation_suite("loan_data_expectations")
    ge_df = ge.from_pandas(df)
    results = ge_df.validate(expectation_suite=suite)

    # Render the results in an HTML format
    html_report = (
        ge.data_context.DataContext()
        .build_data_docs()[0]["local_site"]["site_index_builder"]
        .build()["full_static_asset_html_paths"][0]
    )

    return html_report
