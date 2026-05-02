# Feature Engineering for Battery Dataset

from pathlib import Path
import pandas as pd


# Input and output paths
INPUT_FILE = Path("data/processed/all_batteries_cycles.csv")
OUTPUT_FILE = Path("data/processed/battery_features.csv")


def build_features():
    print("Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    # Sort data properly
    df = df.sort_values(by=["battery_id", "cycle_number"])

    print("Creating features...")

    # ----------------------------------
    # 1. Previous capacity
    # ----------------------------------
    df["previous_capacity"] = df.groupby("battery_id")["capacity"].shift(1)

    # ----------------------------------
    # 2. Capacity drop
    # ----------------------------------
    df["capacity_drop"] = df["previous_capacity"] - df["capacity"]

    # ----------------------------------
    # 3. Capacity drop percentage
    # ----------------------------------
    df["capacity_drop_pct"] = df["capacity_drop"] / df["previous_capacity"]

    # ----------------------------------
    # 4. Rolling average (window=5 cycles)
    # ----------------------------------
    df["capacity_rolling_avg"] = (
        df.groupby("battery_id")["capacity"]
        .rolling(window=5)
        .mean()
        .reset_index(0, drop=True)
    )

    # ----------------------------------
    # 5. Cycle age (normalized)
    # ----------------------------------
    max_cycles = df.groupby("battery_id")["cycle_number"].transform("max")

    df["cycle_age"] = df["cycle_number"] / max_cycles

    # ----------------------------------
    # 6. Temperature deviation
    # ----------------------------------
    mean_temp = df.groupby("battery_id")["avg_temperature_measured"].transform("mean")

    df["temp_deviation"] = df["avg_temperature_measured"] - mean_temp

    print("Saving feature dataset...")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("Feature engineering completed!")
    print(f"Saved file: {OUTPUT_FILE}")

    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    build_features()