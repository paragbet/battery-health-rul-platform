# Multi-file ETL for NASA Battery Dataset
# This script processes all .mat files and combines them into one CSV.

from pathlib import Path
import pandas as pd

# Import the working function from your single-file ETL script
from src.ingest.extract_nasa_cycles import extract_cycles_from_mat


# Folder where all NASA .mat files are stored
RAW_DATA_FOLDER = Path("data/raw/nasa")

# Final combined output file
OUTPUT_FILE = Path("data/processed/all_batteries_cycles.csv")


def extract_all_batteries():
    """
    Find all NASA .mat files, process them one by one,
    and combine them into one DataFrame.
    """

    # Find all .mat files inside raw NASA folder
    mat_files = list(RAW_DATA_FOLDER.glob("**/*.mat"))

    print(f"Number of .mat files found: {len(mat_files)}")

    # This list will store DataFrames from each battery
    all_dataframes = []

    # This list will store files that failed
    failed_files = []

    # Process each .mat file
    for index, file_path in enumerate(mat_files, start=1):
        print(f"\nProcessing file {index} of {len(mat_files)}:")
        print(file_path)

        try:
            # Use your existing ETL function
            df = extract_cycles_from_mat(file_path)

            # Add source file column for traceability
            df["source_file"] = str(file_path)

            # Store this battery dataframe
            all_dataframes.append(df)

            print(f"Success: extracted {len(df)} rows")

        except Exception as error:
            # If one file fails, do not stop the full pipeline
            failed_files.append((str(file_path), str(error)))
            print(f"Failed: {error}")

    # Combine all successful DataFrames
    if len(all_dataframes) == 0:
        raise ValueError("No battery files were successfully processed.")

    combined_df = pd.concat(all_dataframes, ignore_index=True)

    print("\nMulti-file ETL summary:")
    print(f"Files processed successfully: {len(all_dataframes)}")
    print(f"Files failed: {len(failed_files)}")
    print(f"Total rows extracted: {len(combined_df)}")

    if failed_files:
        print("\nFailed files:")
        for file_path, error in failed_files:
            print(f"- {file_path}: {error}")

    return combined_df


if __name__ == "__main__":
    print("Running multi-file NASA battery ETL...")

    # Run extraction
    final_df = extract_all_batteries()

    # Create output folder if needed
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save final combined CSV
    final_df.to_csv(OUTPUT_FILE, index=False)

    print("\nCombined ETL completed successfully!")
    print(f"Saved file: {OUTPUT_FILE}")

    print("\nPreview:")
    print(final_df.head())

    print("\nBattery IDs found:")
    print(final_df["battery_id"].unique())

    print("\nCycle type counts:")
    print(final_df["cycle_type"].value_counts())