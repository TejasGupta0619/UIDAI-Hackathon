#imports

import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.impute import KNNImputer

# Load data

def load_dataset(folder):
    return pd.concat(
        [pd.read_csv(f) for f in Path(folder).glob("*.csv")],
        ignore_index=True
    )

# Date parsing

def parse_date_safe(df):
    df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")

    df["year"] = df["date_parsed"].dt.year
    df["month"] = df["date_parsed"].dt.month

    df["period"] = np.where(
        df["date_parsed"].isna(),
        "UNKNOWN",
        df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
    )

    return df

# Type enforcement

def enforce_numeric(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df[c] = df[c].clip(lower=0)
    return df


# Fix the missing values using Knn imputer 

def impute_counts(df, cols):
    imputer = KNNImputer(n_neighbors=5, weights="distance")
    df[cols] = imputer.fit_transform(df[cols])
    df[cols] = df[cols].round().astype(int)
    return df

# enforce_and_impute

def enforce_and_impute(df, cols):
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    imputer = KNNImputer(n_neighbors=5, weights="distance")
    df[cols] = imputer.fit_transform(df[cols])

    df[cols] = df[cols].round().astype(int)
    return df

# Aggregation

def aggregate_monthly(df, cols):
    df = (
        df.groupby(["state", "district", "year", "month"], as_index=False)
        .agg({c: "sum" for c in cols})
    )
    df["total_activity"] = df[cols].sum(axis=1)
    return df

# Text normalization 

def normalize_text(x):
    if pd.isna(x):
        return None
    return (
        str(x)
        .strip()
        .lower()
        .replace(" ", "")
    )

# Normalize Pin code

def normalize_postal_json(postal_data):
    if isinstance(postal_data, dict):
        return postal_data

    if isinstance(postal_data, list):
        merged = {}
        for item in postal_data:
            if isinstance(item, dict):
                merged.update(item)
        return merged

    raise ValueError("Unsupported postal JSON format")

# Build pin lookup

def build_pin_lookup(postal_data):
    postal_data = normalize_postal_json(postal_data)

    records = []

    for pin, offices in postal_data.items():
        if not offices or not isinstance(offices, list):
            continue

        try:
            office = offices[0]  # canonical
            records.append({
                "pincode": int(pin),
                "state": office["statename"].replace('"', '').strip().upper(),
                "district": office["district"].replace('"', '').strip().upper()
            })
        except Exception:
            continue

    return pd.DataFrame(records)

def apply_pin_recovery(df, pin_lookup_df):
    df["pincode"] = pd.to_numeric(df["pincode"], errors="coerce").astype("Int64")

    df = df.merge(
        pin_lookup_df,
        on="pincode",
        how="left",
        suffixes=("", "_pin")
    )

    # overwrite unreliable CSV text
    df["state"] = df["state_pin"]
    df["district"] = df["district_pin"]

    df = df.drop(columns=["state_pin", "district_pin"])

    # discard unrecoverable rows
    df = df.dropna(subset=["state", "district", "pincode"])

    return df

# Recover the data as much as possible

def recover_geography(row):
    pin = row["pincode"]
    pin_info = fetch_pin_info(pin)

    if pin_info is None:
        return None  # unrecoverable

    row["state"] = pin_info["State"]
    row["district"] = pin_info["District"]
    return row

# Validate the data and recover the possible ones

def validate_and_recover(df):
    recovered = []
    discarded = []

    for _, row in df.iterrows():
        try:
            # PIN validation
            pin = int(row["pincode"])
            if len(str(pin)) != 6:
                discarded.append(row)
                continue

            row = recover_geography(row)
            if row is None:
                discarded.append(row)
                continue

            recovered.append(row)

        except Exception:
            discarded.append(row)

    return pd.DataFrame(recovered), pd.DataFrame(discarded)


# Load json zip data

POSTAL_JSON_PATH = "./sample_datasets/postal_code_data/postal_code_data.json"

with open(POSTAL_JSON_PATH, "r", encoding="utf-8") as f:
    postal_data = json.load(f)

pin_lookup_df = build_pin_lookup(postal_data)

df_enrol = load_dataset("./sample_datasets/api_data_aadhar_enrolment")
df_enrol = parse_date_safe(df_enrol)
df_enrol = apply_pin_recovery(df_enrol, pin_lookup_df)

enrol_cols = ["age_0_5", "age_5_17", "age_18_greater"]
df_enrol = enforce_and_impute(df_enrol, enrol_cols)

df_enrol_monthly = (
    df_enrol[df_enrol["period"] != "UNKNOWN"]
    .groupby(["state", "district", "year", "month"], as_index=False)
    .agg({c: "sum" for c in enrol_cols})
)

df_enrol_monthly["total_enrolment"] = df_enrol_monthly[enrol_cols].sum(axis=1)

df_demo = load_dataset("./sample_datasets/api_data_aadhar_demographic")
df_demo = parse_date_safe(df_demo)
df_demo = apply_pin_recovery(df_demo, pin_lookup_df)

demo_cols = ["demo_age_5_17", "demo_age_17_"]
df_demo = enforce_and_impute(df_demo, demo_cols)

df_demo_monthly = (
    df_demo[df_demo["period"] != "UNKNOWN"]
    .groupby(["state", "district", "year", "month"], as_index=False)
    .agg({c: "sum" for c in demo_cols})
)

df_demo_monthly["total_demographic_updates"] = df_demo_monthly[demo_cols].sum(axis=1)
df_bio = load_dataset("./sample_datasets/api_data_aadhar_biometric")
df_bio = parse_date_safe(df_bio)
df_bio = apply_pin_recovery(df_bio, pin_lookup_df)

bio_cols = ["bio_age_5_17", "bio_age_17_"]
df_bio = enforce_and_impute(df_bio, bio_cols)

df_bio_monthly = (
    df_bio[df_bio["period"] != "UNKNOWN"]
    .groupby(["state", "district", "year", "month"], as_index=False)
    .agg({c: "sum" for c in bio_cols})
)

df_bio_monthly["total_biometric_updates"] = df_bio_monthly[bio_cols].sum(axis=1)

most_active_period = {
    "enrolment": df_enrol_monthly
        .groupby(["year", "month"])["total_enrolment"].sum().idxmax(),

    "demographic": df_demo_monthly
        .groupby(["year", "month"])["total_demographic_updates"].sum().idxmax(),

    "biometric": df_bio_monthly
        .groupby(["year", "month"])["total_biometric_updates"].sum().idxmax(),
}

state_matrix = (
    df_enrol_monthly
    .groupby("state")["total_enrolment"]
    .sum()
    .to_frame("enrolment")
    .join(
        df_demo_monthly.groupby("state")["total_demographic_updates"].sum()
    )
    .join(
        df_bio_monthly.groupby("state")["total_biometric_updates"].sum()
    )
    .fillna(0)
)

enrol_category_distribution = df_enrol_monthly[enrol_cols].sum()

demo_category_distribution = df_demo_monthly[demo_cols].sum()

bio_category_distribution = df_bio_monthly[bio_cols].sum()


print(most_active_period)
print(state_matrix)
print(enrol_category_distribution)
print(demo_category_distribution)
print(bio_category_distribution)