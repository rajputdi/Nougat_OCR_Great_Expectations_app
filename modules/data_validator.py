import great_expectations as ge
from great_expectations.data_context import BaseDataContext
import datetime
import os


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
    results = ge_df.validate()

    # Create a new data context
    context = BaseDataContext()

    # Save the suite and validation results
    suite_name = "my_suite"
    run_id = "batch_" + str(datetime.datetime.utcnow())
    context.save_expectation_suite(expectation_suite=ge_df.get_expectation_suite())
    context.save_validation_result(
        validation_result=results, expectation_suite_name=suite_name, run_id=run_id
    )

    # Build Data Docs
    context.build_data_docs()

    # Get the Data Docs URL for the suite
    local_site_url = context.get_docs_sites_urls(site_name="local_site")[0]["url"]
    suite_url = os.path.join(
        local_site_url, "validations", suite_name, run_id + ".html"
    )

    return suite_url
