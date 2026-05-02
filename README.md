# Battery Health Analytics & RUL Prediction Platform

## Overview

This project is an end-to-end data engineering and machine learning pipeline for analyzing lithium-ion battery degradation and predicting battery capacity using real-world NASA battery datasets.

The system processes raw battery data, builds analytical features, trains machine learning models, and visualizes insights using a dashboard.

---

## Key Features

- ETL pipeline for NASA battery datasets (.mat → structured data)
- Multi-battery scalable data processing
- Feature engineering for degradation analysis
- Machine Learning model for capacity prediction
- PostgreSQL database integration
- Grafana dashboard for visualization
- CI/CD pipeline using GitHub Actions

---

## Tech Stack

- Python (Pandas, NumPy, Scikit-learn)
- PostgreSQL (database)
- Grafana (data visualization)
- Docker (containerization)
- GitHub Actions (CI/CD)

---

## Project Architecture
Raw Data (.mat files)
↓
ETL Pipeline (Python)
↓
Processed CSV Data
↓
PostgreSQL Database
↓
Feature Engineering
↓
Machine Learning Model
↓
Predictions Stored in DB
↓
Grafana Dashboard


---

## Data Source

NASA Battery Aging Dataset:
https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/

---

## Machine Learning

### Problem Type
Regression — Predict battery capacity

### Models Used
- Linear Regression (baseline)
- Random Forest Regressor

### Features Used
- Cycle number
- Voltage (avg)
- Current (avg)
- Temperature (avg)
- Cycle duration
- Cycle age (normalized)
- Temperature deviation

### Evaluation Metrics
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- R² Score

---

## Example Use Case

- Predict battery degradation over lifecycle
- Analyze impact of temperature on battery health
- Compare multiple battery behaviors
- Monitor prediction accuracy in real-time

---

## Dashboard (Grafana)

The dashboard provides:

- Capacity degradation trend
- Voltage trend
- Temperature trend
- Cycle type distribution
- Actual vs Predicted capacity
- Prediction error analysis

(Add screenshots here)

---

## How to Run Locally

### 1. Clone repository
git clone https://github.com/YOUR_USERNAME/battery-health-rul-platform.git

cd battery-health-rul-platform


---

### 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

---

### 3. Run ETL pipeline
python -m src.ingest.extract_all_nasa_cycles

---

### 4. Feature engineering
python src/features/build_features.py

---

### 5. Train ML model
python src/models/train_capacity_model.py

---

### 6. Start PostgreSQL & Grafana
docker compose up -d

---

### 7. Load data into PostgreSQL
python src/db/load_cycles_to_postgres.py

---

### 8. Save predictions to PostgreSQL
python src/models/save_predictions_to_postgres.py

---

### 9. Open Grafana
http://localhost:3000

Login: admin / admin

---

## CI/CD

GitHub Actions pipeline automatically runs unit tests on every push.

---

## Project Highlights

- Built scalable ETL pipeline to process multi-battery datasets
- Designed feature engineering pipeline for battery degradation modeling
- Developed ML model to predict battery capacity using real-world data
- Integrated PostgreSQL for structured storage and querying
- Built interactive Grafana dashboards for data visualization
- Implemented CI/CD pipeline using GitHub Actions

---

## Future Improvements

- Deep learning models (LSTM for time-series prediction)
- Real-time data ingestion
- API layer using FastAPI
- Kubernetes deployment
- Advanced anomaly detection

---

## Author

Parag Betgeri