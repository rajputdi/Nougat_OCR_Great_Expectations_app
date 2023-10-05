import great_expectations as ge
from great_expectations.data_context import BaseDataContext
import datetime
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context import store
from great_expectations.data_context.store import InMemoryStoreBackend
import os


def set_schema_expectations(df):
    # Check for the presence of specific columns
    df.expect_column_to_exist("Credit Score")
    df.expect_column_to_exist("First Payment Date")
    # ... add other columns as needed

    # Check the types of columns
    df.expect_column_values_to_be_of_type("Credit Score", "int")
    df.expect_column_values_to_be_of_type("First Payment Date", "int")
    # ... add other type checks as needed


def create_data_context_config():
    config = DataContextConfig(
        datasources={
            "my_datasource": {
                "data_asset_type": {
                    "class_name": "PandasDataset",
                    "module_name": "great_expectations.dataset",
                },
                "batch_kwargs_generators": {},
                "class_name": "PandasDatasource",
                "module_name": "great_expectations.datasource",
            }
        },
        store_backend_defaults=InMemoryStoreBackend(),
        validation_operators={
            "action_list_operator": {
                "class_name": "ActionListValidationOperator",
                "action_list": [
                    {
                        "name": "store_validation_result",
                        "action": {"class_name": "StoreValidationResultAction"},
                    },
                    {
                        "name": "store_evaluation_params",
                        "action": {"class_name": "StoreEvaluationParametersAction"},
                    },
                    {
                        "name": "update_data_docs",
                        "action": {"class_name": "UpdateDataDocsAction"},
                    },
                ],
            }
        },
        data_docs_sites={
            "local_site": {
                "class_name": "SiteBuilder",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "uncommitted/data_docs/local_site/",
                },
                "site_index_builder": {
                    "class_name": "DefaultSiteIndexBuilder",
                },
            }
        },
    )

    return BaseDataContext(project_config=config)


def validate_dataframe(df):
    # Convert the DataFrame to a GE dataset
    ge_df = ge.from_pandas(df)

    # First, set the schema expectations
    set_schema_expectations(ge_df)

    # Create a new data context
    context = create_data_context_config()

    # Validate the dataframe
    results = ge_df.validate()

    # Create a new data context
    context = BaseDataContext()

    # Save the suite and validation results
    suite_name = "my_suite"
    run_id = "batch_" + str(datetime.datetime.utcnow())
    context.save_expectation_suite(expectation_suite=ge_df.get_expectation_suite())
    context.save_validation_result(
        validation_result=results, expectation_suite_name=suite_name, run_id=run_id
    )

    # Build Data Docs
    context.build_data_docs()

    # Get the Data Docs URL for the suite
    local_site_url = context.get_docs_sites_urls(site_name="local_site")[0]["url"]
    suite_url = os.path.join(
        local_site_url, "validations", suite_name, run_id + ".html"
    )

    return suite_url
