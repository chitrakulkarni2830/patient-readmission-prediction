import sqlite3
import pandas as pd

def run_queries():
    db_path = 'data/hospital.db'
    conn = sqlite3.connect(db_path)
    
    queries = [
        ("1. Count of patients by race", 
         "SELECT race, COUNT(*) as count FROM patients GROUP BY race ORDER BY count DESC;"),
        
        ("2. Average time in hospital by gender", 
         "SELECT gender, AVG(time_in_hospital) as avg_time FROM patients GROUP BY gender;"),
        
        ("3. Readmission rate by age group", 
         "SELECT age, AVG(readmitted_binary) as readmission_rate FROM patients GROUP BY age ORDER BY age;"),
        
        ("4. Top 5 most common primary diagnosis categories", 
         "SELECT diag_1_cat, COUNT(*) as count FROM patients GROUP BY diag_1_cat ORDER BY count DESC LIMIT 5;"),
        
        ("5. Average number of lab procedures for readmitted vs not readmitted", 
         "SELECT readmitted_binary, AVG(num_lab_procedures) as avg_lab_procedures FROM patients GROUP BY readmitted_binary;"),
        
        ("6. Count of patients by insulin usage", 
         "SELECT insulin, COUNT(*) as count FROM patients GROUP BY insulin ORDER BY count DESC;"),
        
        ("7. Patients with high number of emergency visits (>5)", 
         "SELECT COUNT(*) as high_emergency_count FROM patients WHERE number_emergency > 5;"),
        
        ("8. Distribution of A1C results", 
         "SELECT A1Cresult, COUNT(*) as count FROM patients GROUP BY A1Cresult ORDER BY count DESC;"),
        
        ("9. Average procedures by admission source", 
         "SELECT admission_source_group, AVG(num_procedures) as avg_procedures FROM patients GROUP BY admission_source_group;"),
        
        ("10. Max glucose serum levels distribution", 
         "SELECT max_glu_serum, COUNT(*) as count FROM patients GROUP BY max_glu_serum ORDER BY count DESC;")
    ]
    
    for title, sql in queries:
        print(f"\n--- {title} ---")
        try:
            df = pd.read_sql_query(sql, conn)
            print(df)
        except Exception as e:
            print(f"Error: {e}")
            
    conn.close()

if __name__ == "__main__":
    run_queries()
