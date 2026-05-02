# Beginner-friendly and robust ETL for NASA battery dataset
# One row = one battery cycle

from pathlib import Path
import scipy.io
import pandas as pd
import numpy as np


# -----------------------------------
# File paths
# -----------------------------------
INPUT_FILE = Path(
    "data/raw/nasa/5. Battery Data Set/5. BatteryAgingARC_49_50_51_52/B0052.mat"
)

OUTPUT_FILE = Path("data/processed/B0052_cycles.csv")


# -----------------------------------
# Helper functions
# -----------------------------------
def unwrap_object(value):
    """
    Recursively unwrap nested numpy object arrays until
    we reach the actual content.
    """
    while isinstance(value, np.ndarray) and value.dtype == object and value.size == 1:
        value = value.item()
    return value


def to_1d_numeric_array(value):
    """
    Convert a MATLAB-loaded nested value into a 1D numeric numpy array.
    Returns an empty array if conversion fails.
    """
    try:
        value = unwrap_object(value)
        arr = np.array(value, dtype=float).flatten()
        return arr
    except Exception:
        return np.array([], dtype=float)


def to_scalar(value):
    """
    Convert a nested MATLAB-loaded value into a simple Python scalar.
    Returns None if conversion fails.
    """
    try:
        value = unwrap_object(value)

        if isinstance(value, np.ndarray):
            flat = value.flatten()
            if len(flat) == 0:
                return None
            return flat[0]

        return value
    except Exception:
        return None


def to_string(value):
    """
    Convert nested MATLAB-loaded value into string safely.
    """
    value = to_scalar(value)
    if value is None:
        return None
    return str(value)


def safe_mean(arr):
    """
    Return mean of array if it has values, else None.
    """
    if arr is None or len(arr) == 0:
        return None
    return float(np.mean(arr))


def safe_max(arr):
    """
    Return max of array if it has values, else None.
    """
    if arr is None or len(arr) == 0:
        return None
    return float(np.max(arr))


def safe_min(arr):
    """
    Return min of array if it has values, else None.
    """
    if arr is None or len(arr) == 0:
        return None
    return float(np.min(arr))


# -----------------------------------
# Main ETL function
# -----------------------------------
def extract_cycles_from_mat(file_path: Path) -> pd.DataFrame:
    """
    Read one NASA battery .mat file and return a clean DataFrame
    with one row per cycle.
    """

    # Load MATLAB file
    mat_data = scipy.io.loadmat(file_path)

    # Find real battery key such as B0052
    battery_key = [key for key in mat_data.keys() if not key.startswith("__")][0]

    # Extract battery data
    battery_data = mat_data[battery_key]

    # Extract cycle container
    cycle_container = battery_data["cycle"][0, 0]

    # Robustly get cycles
    # In this dataset, the actual cycles are typically inside the first element
    # but this line is kept safe for slight structural variation.
    if isinstance(cycle_container, np.ndarray) and len(cycle_container) == 1:
        cycles = cycle_container[0]
    else:
        cycles = cycle_container

    rows = []
    skipped_cycles = []

    print(f"Battery ID: {battery_key}")
    print(f"Total cycles detected: {len(cycles)}")

    # Loop through cycles
    for i in range(len(cycles)):
        try:
            cycle = cycles[i]

            # -----------------------------
            # Extract cycle metadata
            # -----------------------------
            cycle_type = to_string(cycle["type"])
            ambient_temp = to_scalar(cycle["ambient_temperature"])

            # Start time as raw string
            raw_time = unwrap_object(cycle["time"])
            start_time_raw = str(raw_time)

            # -----------------------------
            # Extract data block
            # -----------------------------
            data_block = unwrap_object(cycle["data"])

            # Some cycles may not contain signal fields in the same way
            # so check safely
            field_names = getattr(data_block, "dtype", None)
            if field_names is None or data_block.dtype.names is None:
                raise ValueError("Cycle data block has no structured fields")

            names = data_block.dtype.names

            # -----------------------------
            # Extract signal arrays
            # -----------------------------
            voltage = to_1d_numeric_array(data_block["Voltage_measured"]) if "Voltage_measured" in names else np.array([])
            current = to_1d_numeric_array(data_block["Current_measured"]) if "Current_measured" in names else np.array([])
            temperature = to_1d_numeric_array(data_block["Temperature_measured"]) if "Temperature_measured" in names else np.array([])
            time_sec = to_1d_numeric_array(data_block["Time"]) if "Time" in names else np.array([])
            current_load = to_1d_numeric_array(data_block["Current_load"]) if "Current_load" in names else np.array([])
            voltage_load = to_1d_numeric_array(data_block["Voltage_load"]) if "Voltage_load" in names else np.array([])
            capacity_arr = to_1d_numeric_array(data_block["Capacity"]) if "Capacity" in names else np.array([])

            # -----------------------------
            # Build one row per cycle
            # -----------------------------
            row = {
                "battery_id": battery_key,
                "cycle_number": i + 1,
                "cycle_type": cycle_type,
                "ambient_temperature": float(ambient_temp) if ambient_temp is not None else None,
                "start_time_raw": start_time_raw,

                # Cycle-level summaries
                "capacity": float(capacity_arr[0]) if len(capacity_arr) > 0 else None,

                "avg_voltage_measured": safe_mean(voltage),
                "min_voltage_measured": safe_min(voltage),
                "max_voltage_measured": safe_max(voltage),

                "avg_current_measured": safe_mean(current),
                "min_current_measured": safe_min(current),
                "max_current_measured": safe_max(current),

                "avg_temperature_measured": safe_mean(temperature),
                "min_temperature_measured": safe_min(temperature),
                "max_temperature_measured": safe_max(temperature),

                "avg_current_load": safe_mean(current_load),
                "avg_voltage_load": safe_mean(voltage_load),

                "duration_seconds": safe_max(time_sec),
                "num_points_voltage": int(len(voltage)),
                "num_points_current": int(len(current)),
                "num_points_temperature": int(len(temperature)),
                "num_points_time": int(len(time_sec)),
            }

            rows.append(row)

        except Exception as e:
            skipped_cycles.append((i + 1, str(e)))
            continue

    df = pd.DataFrame(rows)

    print(f"\nCycles successfully extracted: {len(df)}")
    print(f"Cycles skipped: {len(skipped_cycles)}")

    if skipped_cycles:
        print("\nFirst few skipped cycles:")
        for cycle_no, err in skipped_cycles[:5]:
            print(f"  Cycle {cycle_no}: {err}")

    return df


# -----------------------------------
# Run script
# -----------------------------------
if __name__ == "__main__":
    print("Running extract_nasa_cycles.py ...")

    df_cycles = extract_cycles_from_mat(INPUT_FILE)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_cycles.to_csv(OUTPUT_FILE, index=False)

    print("\nETL completed successfully!")
    print(f"Saved file: {OUTPUT_FILE}")

    print("\nPreview:")
    print(df_cycles.head())

    print("\nColumns:")
    print(df_cycles.columns.tolist())

    if "cycle_type" in df_cycles.columns:
        print("\nCycle type counts:")
        print(df_cycles["cycle_type"].value_counts())