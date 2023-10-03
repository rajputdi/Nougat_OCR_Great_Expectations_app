def correct_credit_score(df):
    invalid_rows = df[~df["Credit Score"].between(300, 850)]
    df.loc[invalid_rows.index, "Credit Score"] = 9999
    return df
