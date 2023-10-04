import streamlit as st
from modules import Uploader, data_processor, data_validator
from ydata_profiling import ProfileReport


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
            with st.spinner("Generating YData Summary..."):
                # Generate the report
                report = ProfileReport(
                    df, title="Data Summary using ydata-profiling", minimal=True
                )
        report.to_file("report.html")
        with open("report.html", "r") as f:
            html_string = f.read()

        st.download_button(
            label="Download Report",
            data=html_string.encode("utf-8"),
            file_name="data_summary_report.html",
            mime="text/html",
        )
        if st.button("Validate with Great Expectations"):
            context = data_validator.initialize_ge_context()
            validation_results = data_validator.validate_data_with_ge(context, df)
            st.write(validation_results)


if __name__ == "__main__":
    main()
