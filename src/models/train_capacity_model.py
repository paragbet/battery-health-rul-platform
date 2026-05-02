# Train a simple Machine Learning model to predict battery capacity

from pathlib import Path
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib


# Input feature file created in Step 6
INPUT_FILE = Path("data/processed/battery_features.csv")

# Folder where trained model will be saved
MODEL_FOLDER = Path("models")

# Output model file
MODEL_FILE = MODEL_FOLDER / "capacity_model.joblib"


def train_model():
    """
    Train ML models to predict battery capacity.
    """

    print("Loading feature dataset...")

    df = pd.read_csv(INPUT_FILE)

    # ----------------------------------
    # Keep only discharge cycles
    # ----------------------------------
    # Capacity is mainly meaningful during discharge cycles.
    df = df[df["cycle_type"] == "discharge"]

    # ----------------------------------
    # Select input features
    # ----------------------------------
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

    # ----------------------------------
    # Remove rows with missing values
    # ----------------------------------
    df = df.dropna(subset=feature_columns + [target_column])

    print(f"Rows available for training: {len(df)}")

    # Input data for ML
    X = df[feature_columns]

    # Output value we want to predict
    y = df[target_column]

    # ----------------------------------
    # Split data into training and test sets
    # ----------------------------------
    # Training data = model learns from this
    # Test data = model is evaluated on unseen data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # ----------------------------------
    # Model 1: Linear Regression
    # ----------------------------------
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    linear_predictions = linear_model.predict(X_test)

    print("\nLinear Regression Results:")
    print_results(y_test, linear_predictions)

    # ----------------------------------
    # Model 2: Random Forest
    # ----------------------------------
    rf_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    rf_model.fit(X_train, y_train)

    rf_predictions = rf_model.predict(X_test)

    print("\nRandom Forest Results:")
    print_results(y_test, rf_predictions)

    # ----------------------------------
    # Save the better model
    # ----------------------------------
    MODEL_FOLDER.mkdir(parents=True, exist_ok=True)

    joblib.dump(rf_model, MODEL_FILE)

    print(f"\nModel saved successfully: {MODEL_FILE}")


def print_results(y_true, y_pred):
    """
    Print model evaluation results.
    """

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print(f"MAE  (Mean Absolute Error): {mae:.4f}")
    print(f"MSE  (Mean Squared Error): {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")


if __name__ == "__main__":
    train_model()