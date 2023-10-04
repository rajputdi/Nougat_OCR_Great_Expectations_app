# data_validator.py

import great_expectations as ge


def create_data_context_in_memory():
    """
    Create a Great Expectations DataContext in memory.
    """
    context = ge.data_context.BaseDataContext(
        project_config={
            "datasources": {
                "pandas_datasource": {
                    "data_asset_type": {"class_name": "PandasDataset"},
                    "class_name": "PandasDatasource",
                    "batch_kwargs_generators": {},
                }
            },
            "stores": {
                "expectations_store": {"class_name": "InMemoryStoreBackend"},
                "validations_store": {"class_name": "InMemoryStoreBackend"},
            },
            "expectation_suite_store": {"class_name": "InMemoryStoreBackend"},
            "validation_operators": {
                "action_list_operator": {
                    "class_name": "ActionListValidationOperator",
                    "action_list": [],
                }
            },
        }
    )
    return context


# data_validator.py continued...


def set_expectations(data_frame, context):
    """
    Set expectations on the dataframe using Great Expectations.
    """
    suite = context.create_expectation_suite(
        expectation_suite_name="suite_name", overwrite_existing=True
    )

    # Add an expectation
    context.add_expectation(
        expectation_suite_name="suite_name",
        expectation_configuration={
            "expectation_type": "expect_column_values_to_be_between",
            "kwargs": {"column": "Credit Score", "min_value": 300, "max_value": 850},
        },
    )

    batch = context.get_batch({"pandas_datasource": data_frame}, "suite_name")

    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[batch]
    )
    return results
