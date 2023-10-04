import great_expectations as ge
from great_expectations.data_context.types.base import DataContextConfig


def initialize_ge_context():
    """
    Initialize a GE DataContext and return it.
    """
    data_context_config = DataContextConfig(
        datasources={
            "my_datasource": {
                "class_name": "PandasDatasource",
                "module_name": "great_expectations.datasource",
                "batch_kwargs_generators": {},
            }
        },
        stores={
            "expectations_store": {
                "class_name": "ExpectationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "/tmp/expectations/",
                },
            },
            "validations_store": {
                "class_name": "ValidationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "/tmp/validations/",
                },
            },
        },
        expectations_store_name="expectations_store",
        validations_store_name="validations_store",
        data_asset_type={
            "module_name": "great_expectations.dataset",
            "class_name": "PandasDataset",
        },
    )

    context = ge.data_context.BaseDataContext(project_config=data_context_config)
    return context


def set_or_update_expectations(context, expectation_suite_name="default_suite"):
    """
    Set or update the expectations for the given context.
    """
    suite = context.get_expectation_suite(
        expectation_suite_name, create_if_not_exist=True
    )

    # Example expectation
    suite.add_expectation(
        {
            "expectation_type": "expect_column_values_to_be_between",
            "kwargs": {"column": "Credit Score", "min_value": 300, "max_value": 850},
        }
    )

    # ... add more expectations as needed ...

    context.save_expectation_suite(suite)
    return suite
