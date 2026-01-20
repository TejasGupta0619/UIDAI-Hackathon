import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from config import DATA_PATHS, SCHEMA_VERSION

from data.postal import build_pin_lookup
from data.dataloader import (
    load_postal_lookup,
    load_monthly_dataset
)

from features.builder import build_features
from features.aggregations import build_state_stats

from outputs.writer import save_state_stats

from questions.engine import answer_question


def run_pipeline():
    # --------------------------------------------------
    # Load postal PIN reference
    # --------------------------------------------------
    pin_lookup_df = load_postal_lookup(
        DATA_PATHS["postal"],
        build_pin_lookup
    )

    # --------------------------------------------------
    # Load & preprocess ENROLMENT
    # --------------------------------------------------
    df_enrol_monthly = load_monthly_dataset(
        DATA_PATHS["enrolment"],
        pin_lookup_df,
        value_columns=["age_0_5", "age_5_17", "age_18_greater"]
    )

    # --------------------------------------------------
    # Load & preprocess DEMOGRAPHIC
    # --------------------------------------------------
    df_demo_monthly = load_monthly_dataset(
        DATA_PATHS["demographic"],
        pin_lookup_df,
        value_columns=["demo_age_5_17", "demo_age_17_"]
    )

    # --------------------------------------------------
    # Load & preprocess BIOMETRIC
    # --------------------------------------------------
    df_bio_monthly = load_monthly_dataset(
        DATA_PATHS["biometric"],
        pin_lookup_df,
        value_columns=["bio_age_5_17", "bio_age_17_"]
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
