import pandas as pd


def process_txt(file):
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

    # Read the .txt file into a DataFrame
    df = pd.read_csv(file, delimiter="|", header=None, names=column_names)

    return df
