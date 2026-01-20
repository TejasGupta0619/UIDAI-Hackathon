import pandas as pd


def normalize_postal_json(postal_data):
    if isinstance(postal_data, dict):
        return postal_data

    merged = {}
    for item in postal_data:
        if isinstance(item, dict):
            merged.update(item)
    return merged


def build_pin_lookup(postal_data):
    postal_data = normalize_postal_json(postal_data)
    records = []

    for pin, offices in postal_data.items():
        if not offices or not isinstance(offices, list):
            continue

        try:
            office = offices[0]
            records.append({
                "pincode": int(pin),
                "pin_state": office["statename"].replace('"', '').strip().upper(),
                "pin_district": office["district"].replace('"', '').strip().upper()
            })
        except Exception:
            continue

    return pd.DataFrame(records)


def apply_pin_recovery(df, pin_lookup_df):
    # Normalize pincode
    df["pincode"] = pd.to_numeric(df["pincode"], errors="coerce").astype("Int64")

    # Merge with lookup
    df = df.merge(
        pin_lookup_df,
        on="pincode",
        how="left"
    )

    # Use PIN-derived geography ONLY
    df["state"] = df["pin_state"]
    df["district"] = df["pin_district"]

    # Drop helper columns
    df = df.drop(columns=["pin_state", "pin_district"])

    # Drop unrecoverable rows
    df = df.dropna(subset=["state", "district", "pincode"])

    return df
