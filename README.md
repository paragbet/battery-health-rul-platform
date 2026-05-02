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
