# Save battery capacity model predictions into PostgreSQL

from pathlib import Path
import pandas as pd
import joblib
from sqlalchemy import create_engine


# -------------------------------
# File paths
# -------------------------------

FEATURE_FILE = Path("data/processed/battery_features.csv")
MODEL_FILE = Path("models/capacity_model.joblib")


# -------------------------------
# PostgreSQL connection settings
# -------------------------------

DB_USER = "battery_user"
DB_PASSWORD = "battery_pass"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "battery_db"

TABLE_NAME = "battery_capacity_predictions"


def save_predictions():
    """
    Load trained model, generate predictions, and save results to PostgreSQL.
    """

    print("Loading feature data...")
    df = pd.read_csv(FEATURE_FILE)

    print("Filtering discharge cycles...")
    df = df[df["cycle_type"] == "discharge"].copy()

    # Same features used during model training
    feature_columns = [
        "cycle_number",
        "avg_voltage_measured",
        "avg_current_measured",
        "avg_temperature_measured",
        "duration_seconds",
        "cycle_age",
        "temp_deviation",
    ]

    target_column = "capacity"

    # Keep only rows where required values exist
    df = df.dropna(subset=feature_columns + [target_column])

    print(f"Rows available for prediction: {len(df)}")

    print("Loading trained model...")
    model = joblib.load(MODEL_FILE)

    print("Generating predictions...")
    X = df[feature_columns]
    predictions = model.predict(X)

    # Create prediction output table
    result_df = pd.DataFrame({
        "battery_id": df["battery_id"],
        "cycle_number": df["cycle_number"],
        "actual_capacity": df[target_column],
        "predicted_capacity": predictions,
    })

    # Error = actual - predicted
    result_df["prediction_error"] = (
        result_df["actual_capacity"] - result_df["predicted_capacity"]
    )

    result_df["absolute_error"] = result_df["prediction_error"].abs()

    # Store model name for traceability
    result_df["model_name"] = "RandomForestRegressor"

    print("Connecting to PostgreSQL...")
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    print("Saving predictions to PostgreSQL...")
    result_df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)

    print("Predictions saved successfully!")
    print(f"Table name: {TABLE_NAME}")
    print(f"Rows saved: {len(result_df)}")

    print("\nPreview:")
    print(result_df.head())


if __name__ == "__main__":
    save_predictions()