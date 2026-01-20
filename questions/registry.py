QUESTION_REGISTRY = {

    # ---- DESCRIPTIVE ----
    "growth_states": {
        "type": "descriptive",
        "description": "States with highest Aadhaar enrolment",
        "metrics": ["total_enrolment"],
        "compute": lambda df, top_n=5:
            df.sort_values("total_enrolment", ascending=False).head(top_n)
    },

    "maintenance_heavy_states": {
        "type": "descriptive",
        "description": "States with highest Aadhaar maintenance workload",
        "metrics": ["maintenance_load"],
        "compute": lambda df, top_n=5:
            df.sort_values("maintenance_load", ascending=False).head(top_n)
    },

    # ---- COMPARATIVE ----
    "future_cost_hotspots": {
        "type": "comparative",
        "description": "States where recurring cost dominates enrolment",
        "metrics": ["maintenance_to_expansion_ratio"],
        "compute": lambda df, top_n=5:
            df.sort_values(
                "maintenance_to_expansion_ratio",
                ascending=False
            ).head(top_n)
    },

    # ---- STRUCTURAL ----
    "mature_vs_growth_states": {
        "type": "structural",
        "description": "States with high maintenance but low enrolment",
        "metrics": ["maintenance_load", "total_enrolment"],
        "compute": lambda df, top_n=5:
            df[df["maintenance_load"] > df["total_enrolment"] * 10]
              .sort_values("maintenance_load", ascending=False)
              .head(top_n)
    }
}
