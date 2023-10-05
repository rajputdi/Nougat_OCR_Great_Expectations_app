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
