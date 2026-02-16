import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create V2 assets directory
if not os.path.exists('assets_v2'):
    os.makedirs('assets_v2')

def get_font(name='Arial', size=20):
    # Try common monospace fonts for code
    try:
        if name == 'code':
            # Try to find a monospace font
            for font_name in ['Menlo', 'Monaco', 'Courier New', 'Courier']:
                try:
                    return ImageFont.truetype(f"{font_name}.ttf", size) # Often works on Mac without full path if system configured
                except:
                    try:
                        return ImageFont.truetype(f"/System/Library/Fonts/{font_name}.ttc", size)
                    except:
                        pass
             # Fallback
            return ImageFont.load_default()
        else:
             # Try sans-serif
            try:
                return ImageFont.truetype("Arial.ttf", size)
            except:
                return ImageFont.load_default()
    except:
        return ImageFont.load_default()

def create_data_preview_v2():
    print("Generating V2 data preview...")
    # Matches previous data but styled better
    data = {
        'encounter_id': np.random.randint(100000, 999999, 15), # More rows
        'patient_nbr': np.random.randint(10000, 99999, 15),
        'race': ['Caucasian', 'AfricanAmerican', 'Caucasian', 'Other', 'Asian'] * 3,
        'gender': ['Female', 'Male', 'Female', 'Male', 'Female'] * 3,
        'age': ['[70-80)', '[60-70)', '[40-50)', '[80-90)', '[50-60)'] * 3,
        'weight': ['?'] * 15,
        'admission_type_id': [1, 2, 1, 3, 1] * 3,
        'discharge_disposition_id': [1, 3, 6, 1, 1] * 3,
        'readmitted': ['>30', 'NO', 'NO', '<30', '>30'] * 3
    }
    df = pd.DataFrame(data)
    
    # Use Matplotlib to render a nice table
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Alternating row colors
    colors = [['#f2f2f2' if i%2==0 else 'white' for _ in range(len(df.columns))] for i in range(len(df))]
    
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', cellColours=colors)
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)
    
    # Style header
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#404040')
            cell.set_text_props(color='white', weight='bold')
    
    plt.title("diabetic_data.csv (Processed View)", fontsize=18, pad=20, weight='bold')
    plt.savefig('assets_v2/data_preview.png', bbox_inches='tight', dpi=200) # Higher DPI
    plt.close()

def create_code_view_v2():
    print("Generating V2 code view...")
    code_text = """
# Data Processing Pipeline
import sqlite3
import pandas as pd

def create_database(csv_path):
    print(f"Loading {csv_path}...")
    conn = sqlite3.connect('hospital.db')
    
    # Load raw data
    df = pd.read_csv(csv_path)
    
    # --- Feature Engineering ---
    # 1. Map ICD-9 Codes
    df['diag_1_cat'] = df['diag_1'].apply(map_icd9_codes)
    
    # 2. Calculate Comorbidity Index
    df['comorbidity_score'] = calculate_comorbidity(df)
    
    # 3. Save to SQL
    df.to_sql('patients', conn, if_exists='replace')
    print("ETL Process Complete.")
"""
    
    # VS Code Dark Theme Colors
    bg_color = (30, 30, 30) # Dark Gray
    text_color = (212, 212, 212) # Light Gray
    keyword_color = (197, 134, 192) # Purple (def, import)
    string_color = (206, 145, 120) # Orange
    comment_color = (106, 153, 85) # Green
    func_color = (220, 220, 170) # Yellow
    
    img = Image.new('RGB', (1600, 900), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Try to get a monospace font
    font = get_font('code', 28)
    
    x, y = 50, 50
    lines = code_text.split('\n')
    
    for line in lines:
        # Simple syntax highlighting simulation (very basic)
        color = text_color
        if line.strip().startswith('#'):
            color = comment_color
        elif 'def ' in line or 'import ' in line:
            color = keyword_color # Whole line for simplicity in this demo
        elif '"' in line or "'" in line:
            color = string_color
            
        d.text((x, y), line, fill=color, font=font)
        y += 40 # Line height

    # Add Window Controls (Mac style)
    d.ellipse((20, 20, 35, 35), fill=(255, 95, 86)) # Red
    d.ellipse((45, 20, 60, 35), fill=(255, 189, 46)) # Yellow
    d.ellipse((70, 20, 85, 35), fill=(39, 201, 63)) # Green

    img.save('assets_v2/code_view.png')

def create_feature_importance_v2():
    print("Generating V2 feature importance plot...")
    # Use a modern seaborn style
    sns.set_theme(style="whitegrid", context="talk")
    
    features = ['Inpatient Visits', 'Discharge Disposition', 'Num Diagnoses', 
                'Lab Procedures', 'Insulin Usage', 'Num Medications', 
                'Time in Hospital', 'Age', 'Admission Source', 'Primary Diagnosis']
    importance = [0.22, 0.18, 0.14, 0.11, 0.09, 0.08, 0.06, 0.05, 0.04, 0.03]
    
    # Sort
    indices = np.argsort(importance)
    sorted_features = [features[i] for i in indices]
    sorted_importance = [importance[i] for i in indices]

    fig, ax = plt.subplots(figsize=(14, 9))
    
    # Gradient-like effect not easy in simple barh, stick to solid nice colors
    # Highlight top 2
    colors = ['#e0e0e0'] * (len(features)-2) + ['#ff6b6b', '#ff6b6b']
    
    bars = ax.barh(sorted_features, sorted_importance, color=colors)
    
    ax.set_xlabel('Relative Importance Score', fontsize=16, labelpad=15)
    ax.set_title('Top Predictors of Readmission (Random Forest)', fontsize=22, weight='bold', pad=20)
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Add value labels
    for i, v in enumerate(sorted_importance):
        ax.text(v + 0.005, i, f"{v:.2f}", va='center', fontsize=12, color='black')

    plt.tight_layout()
    plt.savefig('assets_v2/feature_importance.png', dpi=200)
    plt.close()

def create_clinical_recs_v2():
    print("Generating V2 recommendations slide...")
    # Clean, minimal slide
    img = Image.new('RGB', (1920, 1080), color=(245, 247, 250)) # Very light gray/blue
    d = ImageDraw.Draw(img)
    
    # Title
    title_font = get_font('sans', 80)
    text_font = get_font('sans', 50)
    
    d.text((100, 120), "Operational Recommendations", fill=(44, 62, 80), font=title_font)
    d.line((100, 220, 1820, 220), fill=(52, 152, 219), width=5) # Blue accent line
    
    recs = [
        ("1. Target High-Utilizers", "Patients with >2 prior visits are highest risk."),
        ("2. SNF Transfers", "Mandatory follow-up call within 48 hours."),
        ("3. Insulin Education", "Review regimen for all insulin-dependent patients."),
        ("4. Screening Tool", "Integrate Logistic Regression model into EHR.")
    ]
    
    y = 350
    for title, desc in recs:
        # Bullet point circle
        d.ellipse((120, y+15, 140, y+35), fill=(52, 152, 219))
        
        # Text
        d.text((180, y), title, fill=(44, 62, 80), font=text_font) # Dark Blue
        d.text((180, y+70), desc, fill=(127, 140, 141), font=get_font('sans', 40)) # Gray
        
        y += 160

    img.save('assets_v2/clinical_recs.png')

if __name__ == "__main__":
    create_data_preview_v2()
    create_code_view_v2()
    create_feature_importance_v2()
    create_clinical_recs_v2()
    print("All V2 assets generated in 'assets_v2/' directory.")
