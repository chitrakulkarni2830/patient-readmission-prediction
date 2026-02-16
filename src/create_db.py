import sqlite3
import pandas as pd
import os

def create_database():
    db_path = 'data/hospital.db'
    
    # Connect to (or create) the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load the processed data
    print("Loading processed data into SQLite...")
    df = pd.read_csv('data/processed_data.csv')
    
    # Write to SQL table
    # 'patients' table will contain the main data
    df.to_sql('patients', conn, if_exists='replace', index=False)
    
    print(f"Database created at {db_path}")
    print(f"Table 'patients' created with {len(df)} rows.")
    
    # --- Example Queries ---
    print("\n--- Example SQL Analysis ---")
    
    # Query 1: Readmission Rate by Gender
    query1 = """
    SELECT 
        gender,
        COUNT(*) as total_patients,
        SUM(readmitted_binary) as readmitted_count,
        ROUND(CAST(SUM(readmitted_binary) AS FLOAT) / COUNT(*) * 100, 2) as readmission_rate
    FROM patients
    GROUP BY gender
    ORDER BY readmission_rate DESC;
    """
    print("\nQuery 1: Readmission Rate by Gender")
    print(pd.read_sql_query(query1, conn))
    
    # Query 2: Top 5 Diagnosis Categories with highest readmission volume
    query2 = """
    SELECT 
        diag_1_cat as primary_diagnosis,
        COUNT(*) as total_cases,
        SUM(readmitted_binary) as readmissions
    FROM patients
    WHERE diag_1_cat != 'others'
    GROUP BY diag_1_cat
    ORDER BY readmissions DESC
    LIMIT 5;
    """
    print("\nQuery 2: High Volume Readmission Diagnoses")
    print(pd.read_sql_query(query2, conn))
    
    conn.close()

if __name__ == "__main__":
    create_database()
