import streamlit as st
from modules import Uploader, data_processor, data_validator as dv
from ydata_profiling import ProfileReport
from modules.data_validator import create_data_context_in_memory, set_expectations


def main():
    st.title("Streamlit App with Great Expectations")

    st.write("Upload a file for this session:")
    uploaded_file = Uploader.file_uploader()

    report_type = st.radio(
        "Choose type of report", ["Origination Report", "Monthly Performance Report"]
    )

    if uploaded_file:
        df = data_processor.process_txt(uploaded_file, report_type)

        # Display the dataframe (Top 50 rows) if the "View Data" button is clicked
        if st.button("View Data"):
            st.dataframe(df.head(50))
        if st.button("Generate Data Summary"):
            # Generate the report
            report = ProfileReport(
                df, title="Data Summary using ydata-profiling", minimal=True
            )
        if st.button("Validate with Great Expectations"):
            context = create_data_context_in_memory()
            results = set_expectations(df, context)

    # Display results
    st.write(results)


if __name__ == "__main__":
    main()
