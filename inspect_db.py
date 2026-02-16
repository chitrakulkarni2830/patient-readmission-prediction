
import sqlite3
import pandas as pd
import os

# Assuming the script is run from the project root
db_path = 'data/hospital.db'

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"Tables found: {[t[0] for t in tables]}")
    
    for table_name in tables:
        table = table_name[0]
        print(f"\nSchema for table: {table}")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
            
        # Preview data
        print(f"Preview of {table}:")
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5", conn)
            print(df)
        except Exception as e:
            print(f"Error previewing table {table}: {e}")

    conn.close()

except Exception as e:
    print(f"Error connecting to database: {e}")
