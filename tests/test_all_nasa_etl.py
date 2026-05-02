# Unit tests for combined NASA battery ETL output

from pathlib import Path
import pandas as pd


# Path to combined multi-file ETL output
OUTPUT_FILE = Path("data/processed/all_batteries_cycles.csv")


def load_data():
    """Load the combined ETL output."""
    return pd.read_csv(OUTPUT_FILE)


def test_combined_output_file_exists():
    """Check that the combined ETL output file exists."""
    assert OUTPUT_FILE.exists(), "Combined ETL output file does not exist"


def test_combined_output_has_rows():
    """Check that the combined file is not empty."""
    df = load_data()
    assert len(df) > 0, "Combined ETL output has no rows"


def test_required_columns_exist():
    """Check that important columns are present."""
    df = load_data()

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
        "source_file",
    ]

    for column in required_columns:
        assert column in df.columns, f"Missing required column: {column}"


def test_multiple_batteries_exist():
    """Check that data contains more than one battery."""
    df = load_data()

    battery_count = df["battery_id"].nunique()

    assert battery_count > 1, f"Expected multiple batteries, found only {battery_count}"


def test_cycle_numbers_are_positive():
    """Cycle numbers should be positive."""
    df = load_data()

    assert (df["cycle_number"] > 0).all(), "Some cycle numbers are not positive"


def test_cycle_types_are_valid():
    """Cycle types should only contain expected NASA cycle types."""
    df = load_data()

    valid_types = {"charge", "discharge", "impedance"}

    actual_types = set(df["cycle_type"].dropna().unique())

    assert actual_types.issubset(valid_types), f"Invalid cycle types found: {actual_types}"


def test_source_file_column_not_empty():
    """Each row should contain source file information for traceability."""
    df = load_data()

    assert df["source_file"].notna().all(), "Some rows are missing source_file"


def test_voltage_data_not_completely_empty():
    """Voltage summary should not be completely empty."""
    df = load_data()

    assert df["avg_voltage_measured"].notna().sum() > 0, "Voltage data is completely empty"


def test_temperature_data_not_completely_empty():
    """Temperature summary should not be completely empty."""
    df = load_data()

    assert df["avg_temperature_measured"].notna().sum() > 0, "Temperature data is completely empty"


def test_voltage_values_are_reasonable():
    """Average voltage should be within a reasonable battery-cell range."""
    df = load_data()

    voltage = df["avg_voltage_measured"].dropna()

    assert ((voltage > 0) & (voltage < 10)).all(), "Voltage values are outside expected range"


def test_temperature_values_are_reasonable():
    """Average temperature should be within a reasonable engineering range."""
    df = load_data()

    temperature = df["avg_temperature_measured"].dropna()

    assert ((temperature > -20) & (temperature < 120)).all(), "Temperature values are outside expected range"


def test_duration_is_non_negative():
    """Cycle duration should not be negative."""
    df = load_data()

    duration = df["duration_seconds"].dropna()

    assert (duration >= 0).all(), "Some duration values are negative"