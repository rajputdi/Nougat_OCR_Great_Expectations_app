import streamlit as st
from modules import Uploader, data_processor

# ... other imports ...


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
            with st.spinner("Generating report..."):
                report = data_processor.generate_profiling_report(df)
            html = report.to_html()
            st.success("Report generated!")

            st.download_button(
                label="Download Data Summary Report",
                data=html.encode("utf-8"),
                file_name="data_summary.html",
                mime="text/html",
            )


if __name__ == "__main__":
    main()
