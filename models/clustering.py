import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


def cluster_states(
    state_stats: pd.DataFrame,
    n_clusters: int = 4,
    random_state: int = 42
):
    feature_cols = [
        "total_enrolment",
        "total_demographic_updates",
        "total_biometric_updates",
        "maintenance_to_expansion_ratio",
    ]

    X = state_stats[feature_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init="auto"
    )

    state_stats = state_stats.copy()
    state_stats["cluster"] = kmeans.fit_predict(X_scaled)

    # Centroid interpretation table
    centroid_summary = (
        state_stats
        .groupby("cluster")[feature_cols]
        .mean()
        .round(2)
    )


    cluster_summary = (
        state_stats
        .groupby("cluster")
        .agg({
            "total_enrolment": "mean",
            "total_demographic_updates": "mean",
            "total_biometric_updates": "mean",
            "maintenance_load": "mean",
            "maintenance_to_expansion_ratio": "mean"
        })
        .round(2)
    )

    print(cluster_summary)

    return state_stats, centroid_summary