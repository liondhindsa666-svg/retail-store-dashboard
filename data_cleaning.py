import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = "data/Retail-Store-Transactions_Dashboard.xlsx"
OUTPUT_FILE = "data/cleaned_transactions.csv"

def clean_data(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    df = pd.read_excel(input_file)

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )

    df = df.drop_duplicates().copy()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(["nan", "None", "null", ""], np.nan)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"].astype(str), errors="coerce").dt.time

    for col in ["storeid", "quantity", "unitprice", "totalprice"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "quantity" in df.columns and "unitprice" in df.columns:
        calc_total = df["quantity"] * df["unitprice"]
        if "totalprice" in df.columns:
            df["totalprice"] = df["totalprice"].fillna(calc_total)
            df.loc[df["totalprice"] <= 0, "totalprice"] = calc_total
        else:
            df["totalprice"] = calc_total

    for col in df.columns:
        if df[col].isna().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                mode_val = df[col].mode(dropna=True)
                df[col] = df[col].fillna(mode_val.iloc[0] if not mode_val.empty else "Unknown")

    if "dayofweek" in df.columns:
        df["dayofweek"] = df["dayofweek"].astype(str).str.title()

    if "timeofday" in df.columns:
        df["timeofday"] = df["timeofday"].astype(str).str.title()

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    return df

if __name__ == "__main__":
    clean_data()
    print(f"Cleaned file saved to: {OUTPUT_FILE}")