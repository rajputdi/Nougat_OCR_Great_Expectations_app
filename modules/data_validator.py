import great_expectations as ge


def set_schema_expectations(df):
    # Check for the presence of specific columns
    df.expect_column_to_exist("Credit Score")
    df.expect_column_to_exist("First Payment Date")
    # ... add other columns as needed

    # Check the types of columns
    df.expect_column_values_to_be_of_type("Credit Score", "int")
    df.expect_column_values_to_be_of_type("First Payment Date", "int")
    # ... add other type checks as needed


def validate_dataframe(df):
    # Convert the DataFrame to a GE dataset
    ge_df = ge.from_pandas(df)

    # First, set the schema expectations
    set_schema_expectations(ge_df)
    # Validate the dataframe
    validation_results = ge_df.validate()
    # Fetch expectations
    expectations = ge_df.get_expectation_suite(discard_failed_expectations=False)

    return validation_results, expectations
