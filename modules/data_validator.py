import great_expectations as ge
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.data_context import BaseDataContext
from great_expectations.dataset import PandasDataset


def initialize_ge_context():
    """
    Initialize an in-memory GE context.
    """
    # Create a new in-memory DataContext
    data_context_config = DataContextConfig(
        datasources={
            "in_memory_datasource": {
                "data_asset_type": {"class_name": "PandasDataset"},
                "class_name": "PandasDatasource",
                "module_name": "great_expectations.datasource",
                "batch_kwargs_generators": {},
            }
        },
        store_backendDefaults={"class_name": "InMemoryStoreBackend"},
        validation_operators={
            "action_list_operator": {
                "class_name": "ActionListValidationOperator",
                "action_list": [],
            }
        },
    )

    context = ge.get_context(project_config=data_context_config)
    return context


def set_or_update_expectations(context, df):
    """
    Set or update expectations.
    This function creates new expectations for a dataset.
    """
    batch = ge.dataset.PandasDataset(
        df, expectation_suite=context.get_expectation_suite("default")
    )
    batch.expect_column_values_to_be_between("Credit Score", 300, 850)
    # Add more expectations as needed

    context.save_expectation_suite(batch.get_expectation_suite())
    return batch
