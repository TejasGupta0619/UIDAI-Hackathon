import json
from pathlib import Path

import pandas as pd

from data.preprocessing import (
    load_dataset,
    parse_date_safe,
    enforce_and_impute
)
from data.postal import apply_pin_recovery


# --------------------------------------------------
# Postal reference loader
# --------------------------------------------------
def load_postal_lookup(postal_path, build_pin_lookup_fn):
    postal_path = Path(postal_path)

    if not postal_path.exists():
        raise FileNotFoundError(f"Postal reference file not found: {postal_path}, Extract or download the dataset.")

    with open(postal_path, "r", encoding="utf-8") as f:
        postal_data = json.load(f)

    return build_pin_lookup_fn(postal_data)


# --------------------------------------------------
# Safe CSV loader (handles empty folders)
# --------------------------------------------------
def safe_load_dataset(folder):
    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(f"Data folder does not exist: {folder}, Extract or download the dataset.")

    csv_files = list(folder.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in folder: {folder.resolve()}, Extract or download the dataset."
        )

    return pd.concat(
        (pd.read_csv(f) for f in csv_files),
        ignore_index=True
    )


# --------------------------------------------------
# Generic monthly dataset loader
# --------------------------------------------------
def load_monthly_dataset(
    data_path,
    pin_lookup_df,
    value_columns,
    group_cols=("state", "district", "year", "month")
):
    # ---- Load safely
    df = safe_load_dataset(data_path)

    # ---- Standard preprocessing
    df = parse_date_safe(df)
    df = apply_pin_recovery(df, pin_lookup_df)
    df = enforce_and_impute(df, value_columns)

    # ---- Monthly aggregation
    df_monthly = (
        df[df["period"] != "UNKNOWN"]
        .groupby(list(group_cols), as_index=False)
        .agg({c: "sum" for c in value_columns})
    )

    return df_monthly
