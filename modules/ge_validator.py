import great_expectations as ge
from great_expectations.data_context.types.base import DataContextConfig
import tempfile


def get_in_memory_data_context():
    """
    This creates a basic in-memory GE DataContext.
    """
    data_context_config = {
        "datasources": {
            "pandas_source": {
                "data_asset_type": {
                    "class_name": "PandasDataset",
                    "module_name": "great_expectations.dataset",
                },
                "class_name": "PandasDatasource",
                "module_name": "great_expectations.datasource",
            }
        }
    }

    temp_dir = tempfile.mkdtemp()
    context = ge.data_context.DataContext(context_root_dir=temp_dir)
    context._project_config = data_context_config
    return context


def validate_dataframe(df, context):
    """
    This function takes in a DataFrame and validates it using the given context.
    """
    batch = context.get_batch({"dataset": df}, "default")
    results = batch.validate()
    return results
