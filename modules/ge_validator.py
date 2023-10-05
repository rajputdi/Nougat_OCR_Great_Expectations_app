# ge_validator.py

import great_expectations as ge
from great_expectations.data_context.types.base import (
    DataContextConfig,
    InMemoryStoreBackendDefaults,
)
from great_expectations.data_context import EphemeralDataContext


def initialize_ge_context():
    project_config = DataContextConfig(
        store_backend_defaults=InMemoryStoreBackendDefaults()
    )
    context = EphemeralDataContext(project_config=project_config)
    return context


def add_expectations_to_default_suite(context, df):
    # Retrieve the default suite
    suite = context.get_expectation_suite("default")

    # Convert df into a GE dataset
    ge_df = ge.from_pandas(df)
    ge_df.set_default_expectation_argument("result_format", "BASIC")

    # Add an example expectation: expecting the "Credit Score" column values to be between 300 and 850
    ge_df.expect_column_values_to_be_between(
        "Credit Score", min_value=300, max_value=850
    )

    # Save the updated suite back to the context
    context.save_expectation_suite(suite)
    return suite


def validate_dataframe(df):
    """
    This function validates the dataframe using Great Expectations with the default expectation suite.
    It returns the validation results.
    """
    # Convert the DataFrame to a GE dataset
    ge_df = ge.from_pandas(df, data_context=initialize_ge_context())

    # Validate the dataframe
    results = ge_df.validate()

    return results


def validate_data_against_suite(context, ge_df):
    """
    Validate the provided Great Expectations dataframe against the default suite.
    """
    results = ge_df.validate(expectation_suite=context.get_expectation_suite())
    return results


# ... You can add more functions or helpers here if needed
