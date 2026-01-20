import pandas as pd
import numpy as np
import json
from sklearn.impute import KNNImputer


def load_dataset(folder):
    """Load and concatenate CSV shards from a folder."""
    return pd.concat(
        [pd.read_csv(f) for f in folder.glob("*.csv")],
        ignore_index=True
    )


def parse_date_safe(df):
    """Parse dates; assign UNKNOWN period if parsing fails."""
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
    df["year"] = df["date_parsed"].dt.year
    df["month"] = df["date_parsed"].dt.month

    df["period"] = np.where(
        df["date_parsed"].isna(),
        "UNKNOWN",
        df["year"].astype("Int64").astype(str) + "-" +
        df["month"].astype("Int64").astype(str).str.zfill(2)
    )
    return df


def enforce_and_impute(df, cols):
    """Ensure numeric columns and impute missing values."""
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    imputer = KNNImputer(n_neighbors=5, weights="distance")
    df[cols] = imputer.fit_transform(df[cols])

    df[cols] = df[cols].round().astype(int)
    return df
