import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for better aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def create_output_dir():
    if not os.path.exists('output'):
        os.makedirs('output')

def get_data(query):
    conn = sqlite3.connect('data/hospital.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_race_distribution():
    print("Plotting Race Distribution...")
    query = "SELECT race, COUNT(*) as count FROM patients GROUP BY race ORDER BY count DESC;"
    df = get_data(query)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='race', data=df, palette='viridis')
    plt.title('Patient Count by Race')
    plt.xlabel('Count')
    plt.ylabel('Race')
    plt.tight_layout()
    plt.savefig('output/1_race_distribution.png')
    plt.close()

def plot_avg_time_hospital_gender():
    print("Plotting Avg Time in Hospital by Gender...")
    query = "SELECT gender, AVG(time_in_hospital) as avg_time FROM patients GROUP BY gender;"
    df = get_data(query)
    # Filter out invalid gender if any
    df = df[df['gender'] != 'Unknown/Invalid']
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x='gender', y='avg_time', data=df, palette='magma')
    plt.title('Average Time in Hospital by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Average Days')
    plt.tight_layout()
    plt.savefig('output/2_avg_time_hospital_gender.png')
    plt.close()

def plot_readmission_by_age():
    print("Plotting Readmission Rate by Age...")
    query = "SELECT age, AVG(readmitted_binary) as readmission_rate FROM patients GROUP BY age ORDER BY age;"
    df = get_data(query)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='age', y='readmission_rate', data=df, marker='o', color='b')
    plt.title('Readmission Rate (<30 days) by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Readmission Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('output/3_readmission_by_age.png')
    plt.close()

def plot_top_diagnosis():
    print("Plotting Top Diagnosis Categories...")
    query = "SELECT diag_1_cat, COUNT(*) as count FROM patients GROUP BY diag_1_cat ORDER BY count DESC LIMIT 5;"
    df = get_data(query)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='diag_1_cat', data=df, palette='crest')
    plt.title('Top 5 Primary Diagnosis Categories')
    plt.xlabel('Count')
    plt.ylabel('Diagnosis Category')
    plt.tight_layout()
    plt.savefig('output/4_top_diagnosis.png')
    plt.close()

def plot_lab_procedures_readmission():
    print("Plotting Lab Procedures vs Readmission...")
    query = "SELECT readmitted_binary, AVG(num_lab_procedures) as avg_lab_procedures FROM patients GROUP BY readmitted_binary;"
    df = get_data(query)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x='readmitted_binary', y='avg_lab_procedures', data=df, palette='rocket')
    plt.title('Average Lab Procedures: Readmitted vs Not')
    plt.xlabel('Readmitted (<30 days)')
    plt.ylabel('Avg Lab Procedures')
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.tight_layout()
    plt.savefig('output/5_lab_procedures_readmission.png')
    plt.close()

def plot_insulin_distribution():
    print("Plotting Insulin Usage Distribution...")
    query = "SELECT insulin, COUNT(*) as count FROM patients GROUP BY insulin ORDER BY count DESC;"
    df = get_data(query)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x='insulin', y='count', data=df, palette='pastel')
    plt.title('Distribution of Insulin Usage')
    plt.xlabel('Insulin Status')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('output/6_insulin_distribution.png')
    plt.close()

def plot_a1c_distribution():
    print("Plotting A1C Result Distribution...")
    query = "SELECT A1Cresult, COUNT(*) as count FROM patients GROUP BY A1Cresult ORDER BY count DESC;"
    df = get_data(query)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x='A1Cresult', y='count', data=df, palette='muted')
    plt.title('Distribution of A1C Results')
    plt.xlabel('A1C Result')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('output/7_a1c_distribution.png')
    plt.close()

def plot_max_glucose_distribution():
    print("Plotting Max Glucose Serum Distribution...")
    query = "SELECT max_glu_serum, COUNT(*) as count FROM patients GROUP BY max_glu_serum ORDER BY count DESC;"
    df = get_data(query)
    
    plt.figure(figsize=(8, 6))
    sns.barplot(x='max_glu_serum', y='count', data=df, palette='dark')
    plt.title('Distribution of Max Glucose Serum Levels')
    plt.xlabel('Max Glucose Serum')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('output/8_max_glucose_distribution.png')
    plt.close()

def main():
    create_output_dir()
    plot_race_distribution()
    plot_avg_time_hospital_gender()
    plot_readmission_by_age()
    plot_top_diagnosis()
    plot_lab_procedures_readmission()
    plot_insulin_distribution()
    plot_a1c_distribution()
    plot_max_glucose_distribution()
    print("All plots generated successfully in 'output/' directory.")

if __name__ == "__main__":
    main()
