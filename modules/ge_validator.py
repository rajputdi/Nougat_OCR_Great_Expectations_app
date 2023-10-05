# ge_validator.py

import os
import tempfile
import great_expectations as ge


def get_in_memory_data_context():
    temp_dir = tempfile.mkdtemp()
    ge_dir = os.path.join(temp_dir, "great_expectations")

    # Initialize the great_expectations directory in the temporary folder
    os.makedirs(ge_dir, exist_ok=True)

    # Configure the DataContext using the in-memory backend
    data_context_config = {
        "config_version": 2,
        "plugins_directory": "/plugins",
        "evaluation_parameter_store_name": "evaluation_parameter_store",
        "validations_store_name": "validations_store",
        "expectations_store_name": "expectation_store",
        "data_docs_sites": {
            "local_site": {
                "class_name": "SiteBuilder",
                "store_backend": {
                    "class_name": "InMemoryStoreBackend",
                },
                "show_how_to_buttons": False,
                "site_index_builder": {"class_name": "DefaultSiteIndexBuilder"},
            }
        },
        "stores": {
            "evaluation_parameter_store": {
                "class_name": "EvaluationParameterInMemoryStore"
            },
            "expectations_store": {
                "class_name": "ExpectationsStore",
                "store_backend": {"class_name": "InMemoryStoreBackend"},
            },
            "validations_store": {
                "class_name": "ValidationsStore",
                "store_backend": {"class_name": "InMemoryStoreBackend"},
            },
        },
        "expectation_suite_name": "default",
        "datasources": {
            "my_datasource": {
                "data_asset_type": {
                    "class_name": "PandasDataset",
                },
                "class_name": "PandasDatasource",
                "batch_kwargs_generators": {},
            }
        },
    }

    context = ge.data_context.DataContext(context_root_dir=ge_dir)
    context._project_config = data_context_config

    return context
