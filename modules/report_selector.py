import streamlit as st


def select_report_type():
    report_options = ["Origination Report", "Monthly Performance Report"]
    choice = st.radio("Type of File", report_options)
    return choice
