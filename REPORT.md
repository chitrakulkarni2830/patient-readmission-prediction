# Hospital Readmission prediction - Project Report

## 1. Executive Summary
This project aims to optimize hospital patient flow by predicting the likelihood of a patient being readmitted within 30 days of discharge. Using the "Diabetes 130-US hospitals" dataset, I developed machine learning models to identify high-risk patients. My analysis reveals that **number of inpatient visits**, **number of lab procedures**, and **discharge disposition** are key drivers of readmission. The Logistic Regression model achieved a **Recall of 55%** for the readmitted class, making it a viable tool for screening high-risk patients for targeted interventions.

## 2. Project Goals & Objectives
*   **Primary Goal**: Build a predictive model to classify patients as "Readmitted < 30 days" or "Not Readmitted".
*   **Secondary Goal**: Identify clinical and demographic features that contribute most to readmission risk.
*   **Operational Goal**: Provide actionable insights to hospital administrators to reduce readmission rates and improve patient care.

## 3. Data Source and Description
*   **Dataset**: Diabetes 130-US hospitals for years 1999-2008 (UCI Machine Learning Repository).
*   **Volume**: ~100,000 patient encounters.
*   **Features**: Patient demographics (age, gender, race), admission details, medical specialty, diagnoses (ICD-9 codes), lab tests, and medications.
*   **Target Variable**: `readmitted` (Categorized into `<30` [Target=1] vs `>30` or `NO` [Target=0]).

## 4. Methodology
### 4.1 Data Preprocessing (`src/preprocessing.py`)
*   **Missing Values**: I dropped columns with excessive missing data (`weight`, `payer_code`, `medical_specialty`) and imputed or dropped rows for minor missingness in demographics.
*   **Categorical Grouping**: 
    *   I regrouped `discharge_disposition_id` and `admission_source_id` into broader categories (e.g., "Home", "Transfer", "Emergency").
    *   I mapped 700+ ICD-9 codes into 9 primary clinical categories (Circulatory, Respiratory, Diabetes, etc.).
*   **Filtering**: I removed invalid gender entries and records with missing primary diagnoses.

### 4.2 Feature Engineering (`src/features.py`)
*   **Comorbidity Score**: I calculated a custom `comorbidity_count` based on unique disease categories across 3 diagnosis columns.
*   **Age Encoding**: I converted age ranges (e.g., `[70-80)`) to numeric midpoints (e.g., `75`).
*   **Encoding**: I applied One-Hot Encoding to categorical variables (Race, Insulin levels, Admission type, etc.) to make them suitable for logistic regression.

### 4.3 Database Integration (`src/create_db.py`, `src/run_10_queries.py`)
*   Processed data is loaded into a **SQLite database** (`hospital.db`).
*   I developed a suite of **10 SQL queries** to perform granular analysis, such as:
    *   Readmission rates by age and gender.
    *   Utilization metrics (average lab procedures per readmission status).
    *   Patient stratification by insulin usage.

## 5. Modeling Approach
I experimented with two primary classification algorithms:

1.  **Logistic Regression**
    *   **Configuration**: `class_weight='balanced'` was used to address the severe class imbalance (Readmitted < 30 days is the minority class).
    *   **Strength**: Highly interpretable; allows me to understand the directional effect of each feature (odds ratios).

2.  **Random Forest Classifier**
    *   **Configuration**: 100 Trees, `class_weight='balanced'`.
    *   **Strength**: Captures non-linear relationships and interactions between features. Provides robust feature importance rankings.

## 6. Results & Evaluation
The dataset is imbalanced (~11% readmitted < 30 days). Thus, **Recall** and **F1-Score** for the positive class (1) are the most critical metrics.

### Model Performance
| Model | Accuracy | Class 1 (Readmitted) Precision | Class 1 (Readmitted) Recall | Class 1 F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | 66% | 0.17 | **0.55** | **0.26** |
| **Random Forest** | **89%** | **0.58** | 0.00 | 0.01 |

**Analysis**:
*   The **Random Forest** achieved high accuracy (89%) but failed to identify the minority class (Recall ~0%), biased towards the majority.
*   The **Logistic Regression** successfully identified **55%** of actual readmissions. While this comes with false positives (low precision), it is the preferred model for a screening tool where missing a high-risk patient is more costly than intervening on a low-risk one.

### Key Drivers of Readmission
My feature importance analysis highlighted the following top predictors:
1.  **Number of Inpatient Visits**: Frequent prior hospitalizations are the strongest predictor of future readmission.
2.  **Discharge Disposition**: Patients discharged to rehab facilities or home health care have different risk profiles than those discharged home.
3.  **Number of Diagnoses**: Higher complexity of conditions correlates with risk.
4.  **Number of Lab Procedures**: Indicative of severity of illness.

## 7. Operational Recommendations
1.  **Target High-Utilizers**: Implement specialized discharge planning for patients with >2 prior inpatient visits in the last year.
2.  **Focus on Transfers**: Patients transferred to skilled nursing facilities (SNFs) should have a follow-up call within 48 hours.
3.  **Diabetes Education**: Since insulin usage patterns were significant, ensuring patients understand their insulin regimen before discharge is critical.
4.  **Deploy Screening Tool**: Integrate the Logistic Regression model into the EHR to flag "High Risk" patients daily for case manager review.

## 8. Conclusion
This project demonstrates that while predicting hospital readmission is challenging due to the complexity of human health, a data-driven approach can successfully identify more than half of the at-risk population. By focusing resources on these identified patients, the hospital can potentially reduce readmission rates and improve patient outcomes.
