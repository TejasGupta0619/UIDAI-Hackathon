from pathlib import Path

BASE_DIR = Path("./sample_datasets")

DATA_PATHS = {
    "enrolment": BASE_DIR / "api_data_aadhar_enrolment",
    "demographic": BASE_DIR / "api_data_aadhar_demographic",
    "biometric": BASE_DIR / "api_data_aadhar_biometric",
    "postal": BASE_DIR / "postal_code_data/postal_code_data.json",
}

SCHEMA_VERSION = "v1.0"
