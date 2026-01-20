def build_state_stats(features):
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

    return state_stats
