def build_features(df_enrol, df_demo, df_bio):
    features = (
        df_enrol
        .merge(df_demo, on=["state", "district", "year", "month"], how="outer")
        .merge(df_bio, on=["state", "district", "year", "month"], how="outer")
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

    return features
