# Unit tests for NASA battery ETL output

from pathlib import Path
import pandas as pd


# Path to the ETL output file
OUTPUT_FILE = Path("data/processed/B0052_cycles.csv")


def test_output_file_exists():
    """Check that ETL creates the output CSV file."""
    assert OUTPUT_FILE.exists(), "ETL output file does not exist"


def test_required_columns_exist():
    """Check that important columns are present in the CSV."""
    df = pd.read_csv(OUTPUT_FILE)

    required_columns = [
        "battery_id",
        "cycle_number",
        "cycle_type",
        "ambient_temperature",
        "capacity",
        "avg_voltage_measured",
        "avg_current_measured",
        "avg_temperature_measured",
        "duration_seconds",
    ]

    for column in required_columns:
        assert column in df.columns, f"Missing required column: {column}"


def test_cycle_numbers_are_positive():
    """Cycle numbers should start from 1 and stay positive."""
    df = pd.read_csv(OUTPUT_FILE)

    assert (df["cycle_number"] > 0).all(), "Some cycle numbers are not positive"


def test_cycle_types_are_valid():
    """Cycle type should only be charge, discharge, or impedance."""
    df = pd.read_csv(OUTPUT_FILE)

    valid_types = {"charge", "discharge", "impedance"}

    actual_types = set(df["cycle_type"].dropna().unique())

    assert actual_types.issubset(valid_types), f"Invalid cycle types found: {actual_types}"


def test_voltage_column_not_empty():
    """Average voltage should not be completely empty."""
    df = pd.read_csv(OUTPUT_FILE)

    assert df["avg_voltage_measured"].notna().sum() > 0, "Voltage column is completely empty"


def test_temperature_column_not_empty():
    """Average temperature should not be completely empty."""
    df = pd.read_csv(OUTPUT_FILE)

    assert df["avg_temperature_measured"].notna().sum() > 0, "Temperature column is completely empty"


def test_voltage_values_are_reasonable():
    """Battery voltage average should be in a realistic range."""
    df = pd.read_csv(OUTPUT_FILE)

    voltage_values = df["avg_voltage_measured"].dropna()

    assert ((voltage_values > 0) & (voltage_values < 10)).all(), "Voltage values are outside expected range"


def test_temperature_values_are_reasonable():
    """Battery temperature should be in a realistic engineering range."""
    df = pd.read_csv(OUTPUT_FILE)

    temp_values = df["avg_temperature_measured"].dropna()

    assert ((temp_values > -20) & (temp_values < 100)).all(), "Temperature values are outside expected range"