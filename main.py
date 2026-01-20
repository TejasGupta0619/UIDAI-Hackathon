import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from config import DATA_PATHS, SCHEMA_VERSION

from data.preprocessing import (
    load_dataset,
    parse_date_safe,
    enforce_and_impute
)
from data.postal import (
    build_pin_lookup,
    apply_pin_recovery
)

from features.builder import build_features
from features.aggregations import build_state_stats

from outputs.writer import save_state_stats

from questions.engine import answer_question


def run_pipeline():
    # --------------------------------------------------
    # Load postal PIN reference
    # --------------------------------------------------
    with open(DATA_PATHS["postal"], "r", encoding="utf-8") as f:
        postal_data = json.load(f)

    pin_lookup_df = build_pin_lookup(postal_data)

    # --------------------------------------------------
    # Load & preprocess ENROLMENT
    # --------------------------------------------------
    df_enrol = load_dataset(DATA_PATHS["enrolment"])
    df_enrol = parse_date_safe(df_enrol)
    df_enrol = apply_pin_recovery(df_enrol, pin_lookup_df)

    enrol_cols = ["age_0_5", "age_5_17", "age_18_greater"]
    df_enrol = enforce_and_impute(df_enrol, enrol_cols)

    df_enrol_monthly = (
        df_enrol[df_enrol["period"] != "UNKNOWN"]
        .groupby(["state", "district", "year", "month"], as_index=False)
        .agg({c: "sum" for c in enrol_cols})
    )

    # --------------------------------------------------
    # Load & preprocess DEMOGRAPHIC
    # --------------------------------------------------
    df_demo = load_dataset(DATA_PATHS["demographic"])
    df_demo = parse_date_safe(df_demo)
    df_demo = apply_pin_recovery(df_demo, pin_lookup_df)

    demo_cols = ["demo_age_5_17", "demo_age_17_"]
    df_demo = enforce_and_impute(df_demo, demo_cols)

    df_demo_monthly = (
        df_demo[df_demo["period"] != "UNKNOWN"]
        .groupby(["state", "district", "year", "month"], as_index=False)
        .agg({c: "sum" for c in demo_cols})
    )

    # --------------------------------------------------
    # Load & preprocess BIOMETRIC
    # --------------------------------------------------
    df_bio = load_dataset(DATA_PATHS["biometric"])
    df_bio = parse_date_safe(df_bio)
    df_bio = apply_pin_recovery(df_bio, pin_lookup_df)

    bio_cols = ["bio_age_5_17", "bio_age_17_"]
    df_bio = enforce_and_impute(df_bio, bio_cols)

    df_bio_monthly = (
        df_bio[df_bio["period"] != "UNKNOWN"]
        .groupby(["state", "district", "year", "month"], as_index=False)
        .agg({c: "sum" for c in bio_cols})
    )

    # --------------------------------------------------
    # Build unified feature table
    # --------------------------------------------------
    features = build_features(
        df_enrol_monthly,
        df_demo_monthly,
        df_bio_monthly
    )

    # --------------------------------------------------
    # State-level aggregation
    # --------------------------------------------------
    state_stats = build_state_stats(features)

    # --------------------------------------------------
    # Clustering (lifecycle segmentation)
    # --------------------------------------------------
    X = state_stats[[
        "total_enrolment",
        "total_demographic_updates",
        "total_biometric_updates",
        "maintenance_to_expansion_ratio"
    ]]

    X_scaled = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=4, random_state=42)
    state_stats["cluster"] = kmeans.fit_predict(X_scaled)

    # --------------------------------------------------
    # Persist outputs
    # --------------------------------------------------
    output_path = save_state_stats(
        state_stats,
        schema_version=SCHEMA_VERSION
    )

    return {
        "status": "success",
        "output_file": output_path,
        "states_processed": int(state_stats.shape[0])
    }


if __name__ == "__main__":
    run_pipeline()
