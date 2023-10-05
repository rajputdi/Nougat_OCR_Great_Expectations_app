# ge_validator.py

import great_expectations as ge
from great_expectations.data_context.types.base import (
    DataContextConfig,
    InMemoryStoreBackendDefaults,
)
from great_expectations.data_context import EphemeralDataContext


def get_ephemeral_data_context():
    """
    This function returns an ephemeral data context for Great Expectations.
    """
    project_config = DataContextConfig(
        store_backend_defaults=InMemoryStoreBackendDefaults()
    )
    context = EphemeralDataContext(project_config=project_config)

    return context


def add_expectation_to_default_suite(context):
    """
    Add an expectation for the "Credit Score" column to the default suite.
    """
    # Load the default expectation suite
    suite = context.get_expectation_suite()

    # Add the expectation for the "Credit Score" column
    suite.add_expectation(
        {
            "expectation_type": "expect_column_values_to_be_between",
            "kwargs": {"column": "Credit Score", "min_value": 300, "max_value": 850},
        }
    )

    # Save the updated expectation suite back to the context
    context.save_expectation_suite(suite)

    return suite


def validate_dataframe(df):
    """
    This function validates the dataframe using Great Expectations with the default expectation suite.
    It returns the validation results.
    """
    # Convert the DataFrame to a GE dataset
    ge_df = ge.from_pandas(df, data_context=get_ephemeral_data_context())

    # Validate the dataframe
    results = ge_df.validate()

    return results


# ... You can add more functions or helpers here if needed
