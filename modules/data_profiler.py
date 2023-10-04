import great_expectations as ge
from ydata_profiling import ProfileReport


def profile_data(df):
    ge_df = ge.from_pandas(df)
    profile = ge_df.profile()
    return profile


def generate_profiling_report(df):
    report = ProfileReport(df, title="Data Summary using ydata-profiling", minimal=True)
    return report
