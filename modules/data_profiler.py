import great_expectations as ge


def profile_data(df):
    ge_df = ge.from_pandas(df)
    profile = ge_df.profile()
    return profile
