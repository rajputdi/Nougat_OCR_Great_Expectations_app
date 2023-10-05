import pandas as pd
import great_expectations as ge


def create_suite_from_sample_data(sample_data_path):
    # Load a sample of your data into a DataFrame
    column_names = [
        "Credit Score",
        "First Payment Date",
        "First Time Homebuyer Flag",
        "Maturity Date",
        "Metropolitan Statistical Area (MSA) Or Metropolitan Division",
        "Mortgage Insurance Percentage (MI %)",
        "Number of Units",
        "Occupancy Status",
        "Original Combined Loan-to-Value (CLTV)",
        "Original Debt-to-Income (DTI) Ratio",
        "Original UPB",
        "Original Loan-to-Value (LTV)",
        "Original Interest Rate",
        "Channel",
        "Prepayment Penalty Mortgage (PPM) Flag",
        "Amortization Type (Formerly Product Type)",
        "Property State",
        "Property Type",
        "Postal Code",
        "Loan Sequence Number",
        "Loan Purpose",
        "Original Loan Term",
        "Number of Borrowers",
        "Seller Name",
        "Servicer Name",
        "Super Conforming Flag",
        "Pre-HARP Loan Sequence Number",
        "Program Indicator",
        "HARP Indicator",
        "Property Valuation Method",
        "Interest Only (I/O) Indicator",
        "Mortgage Insurance Cancellation Indicator",
    ]
    df = pd.read_csv(sample_data_path, delimiter="|", header=None, names=column_names)
    context = ge.data_context.DataContext()

    # Create a new expectation suite
    suite_name = "freddie_mac_expectation_suite"
    context.create_expectation_suite(suite_name, overwrite_existing=True)

    # Convert the pandas DataFrame to a Great Expectations dataset
    ge_df = ge.from_pandas(df)

    # Here, we'll define a simple expectation as an example
    # You should replace this with the actual expectations you want
    ge_df.expect_column_to_exist("Credit Score")

    # ... add more expectations as needed ...

    # Save the expectations to the suite
    ge_df.save_expectation_suite(discard_failed_expectations=False)

    print(f"Expectation suite '{suite_name}' created successfully!")


if __name__ == "__main__":
    # Path to your sample data
    sample_data_path = "modules\historical_data_2022Q4.txt"
    create_suite_from_sample_data(sample_data_path)
