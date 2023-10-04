import great_expectations as ge
from great_expectations.data_context.types.base import DataContextConfig

# Your existing imports and functions ...


def initialize_ge_context():
    """
    Initialize a GE DataContext in memory and return it.
    """
    data_context_config = DataContextConfig(
        datasources={
            "my_datasource": {
                "class_name": "PandasDatasource",
                "module_name": "great_expectations.datasource",
            }
        },
        store_backendDefaults={"class_name": "InMemoryStoreBackend"},
        expectations_store_name="expectations_store",
        validations_store_name="validations_store",
        evaluation_parameter_store_name="evaluation_parameter_store",
    )
    return ge.data_context.DataContext(project_config=data_context_config)


def validate_data_with_ge(context, dataframe, suite_name="default"):
    """
    Validate the dataframe using Great Expectations and return the validation results.
    """
    # Add the dataframe as the datasource
    context.add_datasource(
        "my_datasource", module_name="pandas", class_name="PandasDatasource"
    )

    batch_kwargs = {
        "datasource": "my_datasource",
        "data_connector": "default_inferred_data_connector_name",
        "data_asset_name": "my_uploaded_data",
    }

    batch = context.get_batch(batch_kwargs, suite_name)

    # Define expectations (this can be expanded)
    batch.expect_column_values_to_be_between(
        column="Credit Score", min_value=300, max_value=850
    )

    # ... Add more expectations as needed ...

    # Validate
    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[batch]
    )
    return results


# Your existing functions ...
