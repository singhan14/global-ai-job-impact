"""
Script to train models and save them for the Streamlit app
Run this script after training your models in the notebook
"""

import pandas as pd
import numpy as np
import pickle
from catboost import CatBoostRegressor, CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, classification_report, confusion_matrix

# Load data
print("Loading data...")
df = pd.read_csv('ai_impact_jobs_2010_2025(2).csv')

# Define leakage columns and base features
leakage_cols = [
    "industry_ai_adoption_stage",
    "automation_risk_score",
    "ai_job_displacement_risk"
]

X_base = df.drop(columns=leakage_cols, errors="ignore")
feature_columns = X_base.columns.tolist()

# Save feature columns
print("Saving feature columns...")
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

# Identify categorical features
cat_features = X_base.select_dtypes(include=["object"]).columns.tolist()

print("\n" + "="*50)
print("TRAINING MODEL 1: INDUSTRY AI ADOPTION STAGE")
print("="*50)

# Model 1: Industry AI Adoption Stage (trained first, no dependencies)
y_adoption = df["industry_ai_adoption_stage"]

X_train, X_test, y_train, y_test = train_test_split(
    X_base,
    y_adoption,
    test_size=0.2,
    random_state=42,
    stratify=y_adoption
)

model_adoption = CatBoostClassifier(
    iterations=800,
    learning_rate=0.05,
    depth=6,
    loss_function="MultiClass",
    random_seed=42,
    verbose=False
)

model_adoption.fit(X_train, y_train, cat_features=cat_features)
y_pred = model_adoption.predict(X_test).ravel()

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
with open('model_adoption.pkl', 'wb') as f:
    pickle.dump(model_adoption, f)
print("✅ Model saved: model_adoption.pkl")

print("\n" + "="*50)
print("TRAINING MODEL 2: AUTOMATION RISK SCORE")
print("="*50)

# Model 2: Automation Risk Score (depends on adoption stage)
X_auto = X_base.copy()
X_auto["industry_ai_adoption_stage"] = model_adoption.predict(X_base).ravel()

y_auto = df["automation_risk_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X_auto,
    y_auto,
    test_size=0.2,
    random_state=42
)

model_automation = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    loss_function="RMSE",
    random_seed=42,
    verbose=False
)

model_automation.fit(
    X_train,
    y_train,
    cat_features=cat_features + ["industry_ai_adoption_stage"]
)

y_pred = model_automation.predict(X_test)

print("R2:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

# Save model
with open('model_automation.pkl', 'wb') as f:
    pickle.dump(model_automation, f)
print("✅ Model saved: model_automation.pkl")

print("\n" + "="*50)
print("TRAINING MODEL 3: AI JOB DISPLACEMENT RISK")
print("="*50)

# Model 3: AI Job Displacement Risk (depends on both previous models)
X_disp = X_auto.copy()
X_disp["automation_risk_score"] = model_automation.predict(X_auto)

y_disp = df["ai_job_displacement_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X_disp,
    y_disp,
    test_size=0.2,
    random_state=42,
    stratify=y_disp
)

model_displacement = CatBoostClassifier(
    iterations=800,
    learning_rate=0.05,
    depth=6,
    loss_function="MultiClass",
    random_seed=42,
    verbose=False
)

model_displacement.fit(
    X_train,
    y_train,
    cat_features=cat_features + ["industry_ai_adoption_stage"]
)

y_pred = model_displacement.predict(X_test).ravel()

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
with open('model_displacement.pkl', 'wb') as f:
    pickle.dump(model_displacement, f)
print("✅ Model saved: model_displacement.pkl")

print("\n" + "="*50)
print("🎉 ALL MODELS TRAINED AND SAVED SUCCESSFULLY!")
print("="*50)
print("\nSaved files:")
print("  - feature_columns.pkl")
print("  - model_adoption.pkl")
print("  - model_automation.pkl")
print("  - model_displacement.pkl")
print("\n✅ Ready to run: streamlit run app.py")
