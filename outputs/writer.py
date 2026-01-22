import json
from pathlib import Path


def save_state_stats(
    state_stats,
    batch_id,
    schema_version="v1.0",
    output_dir="outputs"
):
    """
    Saves the given state_stats to a JSON file.

    Args:
        state_stats (pandas.DataFrame): The state stats to be saved.
        batch_id (str): The batch id to be used in the filename.
        schema_version (str, optional): The schema version to be used in the filename. Defaults to "v1.0".
        output_dir (str, optional): The directory where the output file will be saved. Defaults to "outputs".

    Returns:
        A dictionary containing the status of the operation and the path to the output file.
    """
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"state_stats_{schema_version}_{batch_id}.json"

    if output_path.exists():
        return {
            "status": "skipped",
            "reason": "output_already_exists",
            "path": str(output_path)
        }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            state_stats.reset_index().to_dict(orient="records"),
            f,
            indent=2
        )

    return {
        "status": "written",
        "path": str(output_path)
    }
