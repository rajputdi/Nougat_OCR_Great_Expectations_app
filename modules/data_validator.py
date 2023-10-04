import great_expectations as ge
from great_expectations.dataset import PandasDataset
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig


def get_or_create_expectation_suite(context, suite_name):
    try:
        # Try to load existing suite
        suite = context.get_expectation_suite(suite_name=suite_name)
    except Exception as e:
        # If not found, create a new one
        suite = context.create_expectation_suite(expectation_suite_name=suite_name)
    return suite


def initialize_ge_context():
    context = ge.data_context.BaseDataContext()

    # Ensure the datasource is set up
    context.add_datasource(name="my_pandas_datasource", class_name="PandasDatasource")
    return context


def set_or_update_expectations(df):
    context = initialize_ge_context()
    suite_name = "loan_data_expectations"
    suite = get_or_create_expectation_suite(context, suite_name)

    # Wrap the dataframe in a Great Expectations dataset
    ge_df = PandasDataset(df)

    # Set Expectation
    ge_df.expect_column_values_to_be_between(
        "Credit Score", min_value=300, max_value=850, mostly=0.99
    )

    # ... add more expectations as needed ...

    # Save updated suite
    context.save_expectation_suite(expectation_suite=suite, suite_name=suite_name)

    return ge_df


def validate_data(df):
    context = initialize_ge_context()
    suite_name = "loan_data_expectations"
    suite = get_or_create_expectation_suite(context, suite_name)
    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[(df, suite_name)]
    )
    return results
