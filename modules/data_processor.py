import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport


def process_txt(file, report_type):
    # Define column names based on the report type
    if report_type == "Origination Report":
        column_names = column_names = [
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
    elif report_type == "Monthly Performance Report":
        column_names = [
            "Loan Sequence Number",
            "Monthly Reporting Period",
            "Current Actual UPB",
            "Current Loan Delinquency Status",
            "Loan Age",
            "Remaining Months to Legal Maturity",
            "Defect Settlement Date",
            "Modification Flag",
            "Zero Balance Code",
            "Zero Balance Effective Date",
            "Current Interest Rate",
            "Current Deferred UPB",
            "Due Date of Last Paid Installment (DDLPI)",
            "MI Recoveries",
            "Net Sales Proceeds",
            "Non MI Recoveries",
            "Expenses",
            "Legal Costs",
            "Maintenance and Preservation Costs",
            "Taxes and Insurance",
            "Miscellaneous Expenses",
            "Actual Loss Calculation",
            "Modification Cost",
            "Step Modification Flag",
            "Deferred Payment Plan",
            "Estimated Loan-to-Value (ELTV)",
            "Zero Balance Removal UPB",
            "Delinquent Accrued Interest",
            "Delinquency Due to Disaster",
            "Borrower Assistance Status Code",
            "Current Month Modification Cost",
            "Interest Bearing UPB",
        ]
    else:
        st.error("Invalid report type selected.")
        return

    # Read the .txt file into a DataFrame
    df = pd.read_csv(file, delimiter="|", header=None, names=column_names)

    return df


def generate_profiling_report(df, report_type):
    report = ProfileReport(
        df, title=f"Data Summary using ydata-profiling {report_type}", minimal=True
    )
    return report
