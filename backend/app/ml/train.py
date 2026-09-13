import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, mean_squared_error, mean_absolute_error, r2_score

# Ensure backend directory is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from backend.app.ml.feature_engineering import engineer_features, FEATURE_COLUMNS
except ImportError:
    from feature_engineering import engineer_features, FEATURE_COLUMNS

def train_and_evaluate():
    models_dir = os.path.join(BASE_DIR, "backend", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    data_path = os.path.join(BASE_DIR, "backend", "data", "processed", "clean_data.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed dataset not found at {data_path}. Run generate_dataset.py first.")

    df = pd.read_csv(data_path)
    print(f"Loaded dataset with {len(df)} samples.")

    # Engineer features
    X = engineer_features(df)
    y_class = df["delay_flag"].astype(int)
    y_reg = df["delay_days"].astype(float)

    # Train / Test split
    X_train, X_test, y_train_cls, y_test_cls, y_train_reg, y_test_reg = train_test_split(
        X, y_class, y_reg, test_size=0.20, random_state=42, stratify=y_class
    )

    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples.")

    # 1. Train Random Forest Classifier
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=6,
        min_samples_split=4,
        random_state=42
    )
    clf.fit(X_train, y_train_cls)

    # Evaluate Classifier
    y_pred_cls = clf.predict(X_test)
    y_prob_cls = clf.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test_cls, y_pred_cls)
    prec = precision_score(y_test_cls, y_pred_cls, zero_division=0)
    rec = recall_score(y_test_cls, y_pred_cls, zero_division=0)
    f1 = f1_score(y_test_cls, y_pred_cls, zero_division=0)
    auc = roc_auc_score(y_test_cls, y_prob_cls)

    print(f"Classifier Metrics -> Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}, ROC-AUC: {auc:.4f}")

    # 2. Train Random Forest Regressor
    reg = RandomForestRegressor(
        n_estimators=120,
        max_depth=6,
        min_samples_split=4,
        random_state=42
    )
    reg.fit(X_train, y_train_reg)

    # Evaluate Regressor
    y_pred_reg = reg.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test_reg, y_pred_reg))
    mae = mean_absolute_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)

    print(f"Regressor Metrics -> RMSE: {rmse:.2f} days, MAE: {mae:.2f} days, R2: {r2:.4f}")

    # Save artifacts
    clf_path = os.path.join(models_dir, "delay_classifier.pkl")
    reg_path = os.path.join(models_dir, "delay_regressor.pkl")
    meta_path = os.path.join(models_dir, "feature_metadata.pkl")
    report_path = os.path.join(models_dir, "evaluation_report.json")

    joblib.dump(clf, clf_path)
    joblib.dump(reg, reg_path)
    joblib.dump({
        "feature_columns": FEATURE_COLUMNS,
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }, meta_path)

    report = {
        "dataset": {
            "total_samples": len(df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "split_method": "80/20 Stratified Train-Test Split (random_state=42)",
            "features_count": len(FEATURE_COLUMNS)
        },
        "classifier": {
            "model_type": "RandomForestClassifier",
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4)
        },
        "regressor": {
            "model_type": "RandomForestRegressor",
            "rmse": round(float(rmse), 2),
            "mae": round(float(mae), 2),
            "r2_score": round(float(r2), 4)
        },
        "features": FEATURE_COLUMNS
    }

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Models and evaluation report successfully saved to {models_dir}")


if __name__ == "__main__":
    train_and_evaluate()

