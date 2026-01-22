from pathlib import Path

BASE_DIR = Path("./sample_datasets")

BATCH_ID = "01012026"

DATA_PATHS = {
    "enrolment": BASE_DIR / f"api_data_aadhar_enrolment_{BATCH_ID}",
    "demographic": BASE_DIR / f"api_data_aadhar_demographic_{BATCH_ID}",
    "biometric": BASE_DIR / f"api_data_aadhar_biometric_{BATCH_ID}",
    "postal": BASE_DIR / "postal_code_data/postal_code_data.json",
}

SCHEMA_VERSION = "v1.0"
OUTPUT_DIR = Path("outputs")
