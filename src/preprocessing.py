import pandas as pd
import numpy as np
import os

def preprocess_data(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # 1. Handle missing values represented by '?'
    df.replace('?', np.nan, inplace=True)
    
    # Analyze missingness
    missing_pct = df.isnull().mean() * 100
    print("Missing values percentage per column:")
    print(missing_pct[missing_pct > 0])
    
    # Drop columns with very high missingness
    # Weight is ~97% missing, payer_code ~40% (often irrelevant for clinical prediction), 
    # medical_specialty ~49% (can be useful but highly sparse).
    cols_to_drop = ['weight', 'payer_code', 'medical_specialty']
    df.drop(columns=cols_to_drop, inplace=True, errors='ignore')
    
    # Drop rows with missing values in critical columns (minority of data)
    df.dropna(subset=['race', 'gender', 'diag_1'], inplace=True)
    
    # 2. Group and re-categorize 'Admission Source' and 'Discharge Disposition'
    # Grouping IDs based on clinical/administrative similarity
    
    # Discharge Disposition: Group home-related, transferred, and other/expired
    # 1: Discharged to home
    # 6: Discharged/transferred to home with home health service
    # 8: Discharged/transferred to home under care of Home IV provider
    # 13: Hospice/home
    # 19, 20, 21: Expired (should probably be excluded if we only want to predict survival-readmission, 
    # but for a simple model we can group them as "Not Home")
    
    def group_discharge_disposition(val):
        val = int(val)
        if val in [1, 6, 8]:
            return 'discharged_to_home'
        elif val in [11, 19, 20, 21]:
            return 'expired'
        elif val in [3, 4, 5, 14, 22, 23, 24]:
            return 'transferred_to_facility'
        else:
            return 'other'
            
    df['discharge_disposition_group'] = df['discharge_disposition_id'].apply(group_discharge_disposition)
    
    # Admission Source
    def group_admission_source(val):
        val = int(val)
        if val in [1, 2, 3]:
            return 'referral'
        elif val in [4, 5, 6, 10, 22, 25]:
            return 'transfer'
        elif val == 7:
            return 'emergency'
        else:
            return 'other'
            
    df['admission_source_group'] = df['admission_source_id'].apply(group_admission_source)
    
    # 3. Handle high-cardinality categorical features: Diagnosis codes (ICD-9)
    def categorize_icd9(code):
        if pd.isnull(code):
            return 'others'
        
        # Remove any alphanumeric prefixes (like 'V' or 'E') for primary numeric check
        # But keep track for specific V/E categories if needed
        str_code = str(code)
        if str_code.startswith('V') or str_code.startswith('E'):
            return 'others'
            
        try:
            val = float(code)
        except ValueError:
            return 'others'
            
        if 390 <= val <= 459 or val == 785:
            return 'circulatory'
        elif 460 <= val <= 519 or val == 786:
            return 'respiratory'
        elif 520 <= val <= 579 or val == 787:
            return 'digestive'
        elif 250 <= val < 251: # Exact 250.xx is diabetes
            return 'diabetes'
        elif 800 <= val <= 999:
            return 'injury'
        elif 710 <= val <= 739:
            return 'musculoskeletal'
        elif 580 <= val <= 629 or val == 788:
            return 'genitourinary'
        elif 140 <= val <= 239:
            return 'neoplasms'
        else:
            return 'others'

    df['diag_1_cat'] = df['diag_1'].apply(categorize_icd9)
    df['diag_2_cat'] = df['diag_2'].apply(categorize_icd9)
    df['diag_3_cat'] = df['diag_3'].apply(categorize_icd9)
    
    # 4. Target Variable: Readmitted < 30 days
    # Original values: '<30', '>30', 'NO'
    df['readmitted_binary'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)
    
    # Drop original ID columns to avoid leakage/redundancy
    df.drop(columns=['encounter_id', 'patient_nbr', 'admission_type_id', 
                     'discharge_disposition_id', 'admission_source_id',
                     'diag_1', 'diag_2', 'diag_3', 'readmitted'], inplace=True)
    
    print(f"Preprocessing complete. Shape: {df.shape}")
    df.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}")

if __name__ == "__main__":
    preprocess_data('data/diabetic_data.csv', 'data/processed_data.csv')
