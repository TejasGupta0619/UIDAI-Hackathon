isnt it still less, also now 

organize this code remove the garbage write proper documentation and make it deployment and api response ready.

#imports

import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime

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
        df["year"].astype("Int64").astype(str) + "-" +
        df["month"].astype("Int64").astype(str).str.zfill(2)
    )

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

# Json Normalization 

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

# Build pin lookup for search

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

# Apply pin recovery

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

POSTAL_JSON_PATH = "/content/drive/MyDrive/sample_dataset/postal_code_data/postal_code_data.json"

with open(POSTAL_JSON_PATH, "r", encoding="utf-8") as f:
    postal_data = json.load(f)

pin_lookup_df = build_pin_lookup(postal_data)
print(pin_lookup_df.head())
print("PINs loaded:", len(pin_lookup_df))

df_enrol = load_dataset("/content/drive/MyDrive/sample_dataset/api_data_aadhar_enrolment")
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

df_demo = load_dataset("/content/drive/MyDrive/sample_dataset/api_data_aadhar_demographic")
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

bio_cols = ["bio_age_5_17", "bio_age_17_"]
df_bio = load_dataset("/content/drive/MyDrive/sample_dataset/api_data_aadhar_biometric")
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

features = (
    df_enrol_monthly
    .merge(
        df_demo_monthly,
        on=["state", "district", "year", "month"],
        how="outer"
    )
    .merge(
        df_bio_monthly,
        on=["state", "district", "year", "month"],
        how="outer"
    )
    .fillna(0)
)

features["total_enrolment"] = (
    features["age_0_5"] +
    features["age_5_17"] +
    features["age_18_greater"]
)

features["total_demographic_updates"] = (
    features["demo_age_5_17"] +
    features["demo_age_17_"]
)

features["total_biometric_updates"] = (
    features["bio_age_5_17"] +
    features["bio_age_17_"]
)

features["maintenance_load"] = (
    features["total_demographic_updates"] +
    features["total_biometric_updates"]
)

features["maintenance_to_expansion_ratio"] = (
    features["maintenance_load"] /
    (features["total_enrolment"] + 1)
)

state_stats = (
    features
    .groupby("state")
    .agg({
        "total_enrolment": "sum",
        "total_demographic_updates": "sum",
        "total_biometric_updates": "sum",
        "maintenance_load": "sum"
    })
)

state_stats["maintenance_to_expansion_ratio"] = (
    state_stats["maintenance_load"] /
    (state_stats["total_enrolment"] + 1)
)

QUESTION_REGISTRY = {
    "future_cost_hotspots": {
        "description": "States where recurring Aadhaar maintenance cost is high relative to enrolment",
        "type": "comparative",
        "metrics_used": [
            "maintenance_load",
            "maintenance_to_expansion_ratio"
        ],
        "params": {
            "top_n": 5
        },
        "compute": lambda df, top_n=5: (
            df.sort_values(
                "maintenance_to_expansion_ratio",
                ascending=False
            ).head(top_n)
        )
    },

    "growth_states": {
        "description": "States with highest Aadhaar enrolment activity",
        "type": "descriptive",
        "metrics_used": ["total_enrolment"],
        "params": {
            "top_n": 5
        },
        "compute": lambda df, top_n=5: (
            df.sort_values("total_enrolment", ascending=False)
              .head(top_n)
        )
    },

    "maintenance_heavy_states": {
        "description": "States with highest combined demographic and biometric workload",
        "type": "descriptive",
        "metrics_used": ["maintenance_load"],
        "params": {
            "top_n": 5
        },
        "compute": lambda df, top_n=5: (
            df.sort_values("maintenance_load", ascending=False)
              .head(top_n)
        )
    }
}

def answer_question(
    question_id: str,
    df: pd.DataFrame,
    **params
):
    if question_id not in QUESTION_REGISTRY:
        raise ValueError(f"Unknown question: {question_id}")

    q = QUESTION_REGISTRY[question_id]

    # Merge default params with runtime params
    final_params = q.get("params", {}).copy()
    final_params.update(params)

    result_df = q["compute"](df, **final_params)

    return {
        "question_id": question_id,
        "description": q["description"],
        "type": q["type"],
        "metrics_used": q["metrics_used"],
        "params": final_params,
        "result": result_df.reset_index().to_dict(orient="records")
    }

X = state_stats[[
    "total_enrolment",
    "total_demographic_updates",
    "total_biometric_updates",
    "maintenance_to_expansion_ratio"
]]

X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
state_stats["cluster"] = kmeans.fit_predict(X_scaled)

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

state_stats_json = state_stats.reset_index().to_dict(orient="records")

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

SCHEMA_VERSION = "v1.0"
output_path = (
    f"outputs/state_stats_v{SCHEMA_VERSION}_{timestamp}.json"
)

with open(output_path, "w") as f:
    json.dump(state_stats_json, f, indent=2)

print("df_enrol nunique" , df_enrol["state"].nunique())
print("most_active_period" , most_active_period)
print("state_matrix" , state_matrix)
print("enrol_category_distribution" , enrol_category_distribution)
print("demo_category_distribution" , demo_category_distribution)
print("bio_category_distribution" , bio_category_distribution)
print("df_bio_monthly" , df_bio_monthly)
print("features" , features)
print("state_matrix" , state_matrix)
print("state_stats" , state_stats)
print("QUESTION_MAP" , QUESTION_MAP)