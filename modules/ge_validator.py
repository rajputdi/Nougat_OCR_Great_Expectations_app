# ge_validator.py

import great_expectations as ge
from great_expectations.data_context.types.base import (
    DataContextConfig,
    InMemoryStoreBackendDefaults,
)
from great_expectations.data_context import EphemeralDataContext
from great_expectations.core.batch import BatchRequest


def initialize_ge_context():
    project_config = DataContextConfig(
        store_backend_defaults=InMemoryStoreBackendDefaults()
    )
    context = EphemeralDataContext(project_config=project_config)
    return context


def add_expectations_to_default_suite(context, df):
    # Convert the pandas df into a GE batch
    batch_request = BatchRequest(
        datasource_name="memory",
        data_connector_name="default_inferred_data_connector_name",
        data_asset_name="default_name",
        batch_data=df,
    )
    batch = context.get_batch(batch_request)

    # Create an empty suite or get an existing suite
    suite = context.create_expectation_suite(
        expectation_suite_name="default", overwrite_existing=True
    )

    # Now, let's add some expectations
    batch.expect_column_to_exist("Credit Score")
    # ... add other expectations ...

    # Save the expectations
    context.save_expectation_suite(suite, "default")

    # Validate the dataframe
    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[batch]
    )
    return results


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
