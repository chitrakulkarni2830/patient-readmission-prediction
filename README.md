# Predictive Optimization for Hospital Patient Flow

## Project Overview
A machine learning project to predict the probability of a patient being readmitted to the hospital within 30 days. This project analyzes the "Diabetes 130-US hospitals" dataset to identify high-risk patients and key drivers of readmission.

## Project Demo
[![Hospital Patient Flow Demo](output/hospital_patient_flow_v2.mp4)](output/hospital_patient_flow_v2.mp4)
*Watch the 60-second video overview covering the problem, data engineering, and machine learning results.*

## Goals
- **Predict** 30-day readmission risk.
- **Identify** key features (comorbidities, lab procedures) driving readmission.
- **Provide** a tool for hospital administrators to target interventions.

## Key Outcomes
- **Logistic Regression Recall**: 55% (Success in identifying high-risk patients).
- **Top Predictors**: Number of inpatient visits, number of lab procedures, and diagnosis category.

## Project Structure
- `data/`: Contains raw and processed datasets (CSV and SQLite).
- `src/`:
    - `download_data.py`: Downloads dataset from UCI.
    - `preprocessing.py`: Cleans data, handles missing values, and groups IDs.
    - `features.py`: Creates comorbidity features and performs one-hot encoding.
    - `modeling.py`: Trains Logistic Regression and Random Forest models.
    - `create_db.py`: Loads data into a SQLite database for querying.
    - `run_10_queries.py`: Executes 10 SQL queries to generate insights from the database.
- `output/`: Contains model evaluation reports and feature importance plots.
- `REPORT.md`: Comprehensive project report with detailed methodology and results.

## Video Generation
The project includes scripts to programmatically generate the demo video:
- `scripts/generate_assets_v2.py`: Creates high-quality synthetic assets (code views, charts).
- `scripts/create_video_v2.py`: Assembles the video using `moviepy` with motion effects and transitions.

To regenerate the video:
```bash
python scripts/generate_assets_v2.py
python scripts/create_video_v2.py
```

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the pipeline:
   ```bash
   python3 src/download_data.py
   python3 src/preprocessing.py
   python3 src/features.py
   python3 src/modeling.py
   ```
3. Run SQL analysis:
   ```bash
   python3 src/create_db.py
   python3 src/run_10_queries.py
   ```

## Author
Chitra Kulkarni
