# necessary imports
import great_expectations as ge
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.data_context.types.resource_identifiers import (
    ExpectationSuiteIdentifier,
)
from great_expectations.dataset import PandasDataset

# necessary imports
from great_expectations.data_context.util import (
    instantiate_class_from_config,
)


# Configuration for Great Expectations
def initialize_ge_context():
    project_config = DataContextConfig(
        config_version=2,
        plugins_directory=None,
        config_variables_file_path=None,
        datasources={
            "my_datasource": {
                "class_name": "PandasDatasource",
                "module_name": "great_expectations.datasource",
                "data_asset_type": {
                    "class_name": "PandasDataset",
                    "module_name": "great_expectations.dataset",
                },
            }
        },
        stores={
            "expectations_store": {
                "class_name": "ExpectationsStore",
                "store_backend": {"class_name": "InMemoryStoreBackend"},
            },
            "validations_store": {
                "class_name": "ValidationsStore",
                "store_backend": {"class_name": "InMemoryStoreBackend"},
            },
        },
        expectations_store_name="expectations_store",
        validations_store_name="validations_store",
        data_docs_sites={},
        validation_operators={
            "default": {
                "class_name": "ActionListValidationOperator",
                "action_list": [],
            }
        },
    )

    context = BaseDataContext(project_config=project_config)
    return context


def create_suite(context, suite_name):
    """
    Create a new expectation suite with the given suite_name.
    If suite already exists, return the existing one.
    """
    try:
        suite = context.get_expectation_suite(suite_name=suite_name)
    except KeyError:  # suite not found
        suite = ExpectationSuite(expectation_suite_name=suite_name)
        context.save_expectation_suite(expectation_suite=suite)
    return suite


def set_or_update_expectations(context, df):
    suite_name = "loan_data_expectations"
    suite = context.create_expectation_suite(
        suite_name=suite_name, overwrite_existing=True
    )
    batch = ge.dataset.PandasDataset(df, expectation_suite=suite)

    # Add expectation: Credit Score should be between 300 and 850
    batch.expect_column_values_to_be_between(
        "Credit Score", min_value=300, max_value=850
    )

    # You can add more expectations here

    context.save_expectation_suite(batch.get_expectation_suite())


def validate_data(context, df):
    suite_name = "loan_data_expectations"
    suite = context.get_expectation_suite(suite_name)
    batch = ge.dataset.PandasDataset(df, expectation_suite=suite)
    results = context.run_validation_operator("default", assets_to_validate=[batch])
    return results
