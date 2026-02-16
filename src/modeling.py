import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

def train_and_evaluate(input_path):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Target and Features
    X = df.drop(columns=['readmitted_binary'])
    y = df['readmitted_binary']
    
    # 1. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Train set size: {X_train.shape}, Test set size: {X_test.shape}")
    print(f"Class distribution in training: {np.bincount(y_train)}")
    
    results_dir = 'output'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    # --- Logistic Regression ---
    print("\nTraining Logistic Regression...")
    # Use class_weight='balanced' to handle imbalance
    lr_model = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    print("\nLogistic Regression Classification Report:")
    lr_report = classification_report(y_test, y_pred_lr)
    print(lr_report)
    
    # --- Random Forest ---
    print("\nTraining Random Forest Classifier...")
    # Use class_weight='balanced' here too
    rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    print("\nRandom Forest Classification Report:")
    rf_report = classification_report(y_test, y_pred_rf)
    print(rf_report)
    
    # --- Feature Importance Plot (Random Forest) ---
    print("\nGenerating Feature Importance Plot...")
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[-15:] # Top 15 features
    
    plt.figure(figsize=(10, 8))
    plt.title('Top 15 Predictors for Patient Readmission')
    plt.barh(range(len(indices)), importances[indices], color='skyblue', align='center')
    plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
    plt.xlabel('Relative Importance Score')
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'feature_importance.png'))
    print(f"Feature importance plot saved to {os.path.join(results_dir, 'feature_importance.png')}")
    
    # Save reports to text file for the user
    with open(os.path.join(results_dir, 'model_evaluation_report.txt'), 'w') as f:
        f.write("=== Logistic Regression Report ===\n")
        f.write(lr_report)
        f.write("\n\n=== Random Forest Report ===\n")
        f.write(rf_report)
    
    # Save models
    joblib.dump(lr_model, os.path.join(results_dir, 'logistic_regression_model.pkl'))
    joblib.dump(rf_model, os.path.join(results_dir, 'random_forest_model.pkl'))
    print("Models and reports saved successfully.")

if __name__ == "__main__":
    train_and_evaluate('data/final_features.csv')
