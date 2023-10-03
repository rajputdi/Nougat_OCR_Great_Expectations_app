import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration


def initialize_expectations():
    context = ge.data_context.DataContext()
    try:
        suite = context.get_expectation_suite("loan_data_expectations")
    except ge.exceptions.exceptions.DataContextError:
        suite = context.create_expectation_suite("loan_data_expectations")
        context.save_expectation_suite(suite)
    return suite


def set_credit_score_expectation(suite):
    expectation_configuration = ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={"column": "Credit Score", "min_value": 300, "max_value": 850},
    )
    suite.add_expectation(expectation_configuration)


def generate_profiling_report(df):
    context = ge.data_context.DataContext()
    suite = context.get_expectation_suite("loan_data_expectations")
    ge_df = ge.from_pandas(df)

    batch_kwargs = {"dataset": ge_df, "datasource": "pandas_datasource"}
    batch = context.get_batch(batch_kwargs, suite)
    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[batch]
    )
    validation_results_dict = results.results[batch.batch_id][
        "expectation_suite_results"
    ]
    document = context.build_data_docs(resource_identifiers=[validation_results_dict])
    site_keys = list(context.get_config().data_docs_sites.keys())
    html_url = document[site_keys[0]]
    return html_url
