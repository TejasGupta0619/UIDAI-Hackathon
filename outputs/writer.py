import json
from datetime import datetime
from pathlib import Path


def save_state_stats(state_stats, schema_version="v1.0", output_dir="outputs"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_path = (
        f"{output_dir}/state_stats_{schema_version}_{timestamp}.json"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            state_stats.reset_index().to_dict(orient="records"),
            f,
            indent=2
        )

    return output_path
