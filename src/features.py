import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def feature_engineering(input_path, output_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # 1. Create a feature for 'comorbidity'
    # Defining comorbidity as the count of distinct non-'others' clinical categories
    # across the three primary diagnoses.
    diag_cols = ['diag_1_cat', 'diag_2_cat', 'diag_3_cat']
    
    def calculate_comorbidity(row):
        cats = [row[c] for c in diag_cols if row[c] != 'others']
        return len(set(cats))
        
    df['comorbidity_count'] = df.apply(calculate_comorbidity, axis=1)
    
    # 2. Encode Categorical Features
    # Identify categorical columns
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    print(f"Encoding categorical columns: {cat_cols}")
    
    # Use Label Encoding for models like Random Forest, 
    # but One-Hot for Logistic Regression. 
    # For simplicity and 'Gold Standard' portfolio, we'll use One-Hot Encoding
    # but keep the number of features manageable.
    
    # Group age into numeric (midpoints)
    age_mapping = {
        '[0-10)': 5, '[10-20)': 15, '[20-30)': 25, '[30-40)': 35,
        '[40-50)': 45, '[50-60)': 55, '[60-70)': 65, '[70-80)': 75,
        '[80-90)': 85, '[90-100)': 95
    }
    df['age_numeric'] = df['age'].map(age_mapping)
    df.drop(columns=['age'], inplace=True)
    
    # One-Hot Encoding
    # Note: Many scripts like 'metformin', 'repaglinide' etc. are 'No', 'Steady', 'Up', 'Down'.
    # We should keep them as features.
    
    df_encoded = pd.get_dummies(df, drop_first=True)
    
    print(f"Feature engineering complete. Shape: {df_encoded.shape}")
    df_encoded.to_csv(output_path, index=False)
    print(f"Saved feature-engineered data to {output_path}")

if __name__ == "__main__":
    feature_engineering('data/processed_data.csv', 'data/final_features.csv')
