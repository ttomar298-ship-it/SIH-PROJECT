import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from backend.app.ml.feature_engineering import engineer_features, FEATURE_COLUMNS, STAGE_MAP
    from backend.app.ml.risk_scoring import calculate_calibrated_risk_score
except ImportError:
    from feature_engineering import engineer_features, FEATURE_COLUMNS, STAGE_MAP
    from risk_scoring import calculate_calibrated_risk_score

COST_FEATURE_COLUMNS = [
    "budget_crores",
    "planned_duration_days",
    "compensation_pct",
    "legal_case",
    "affected_families",
    "stage_index",
    "is_rr_pending",
    "is_rr_completed",
    "compensation_deficit",
    "families_per_crore",
    "clr_completed_pct",
    "delay_days",
    "risk_score"
]

def derive_target_overrun_pct(df: pd.DataFrame) -> pd.Series:
    """
    Derives realistic proxy training target for cost overrun percentage (%)
    based on observed project parameters, historical delay escalation, litigation penalties,
    and R&R/land digitalization friction.
    
    Formula:
      delay_escalation = 10.0 * (delay_days / 365.0).clip(0, 2.5)  # ~10% cost inflation per year of delay
      litigation_penalty = 8.0 * legal_case                         # ~8% statutory interest & court stay cost
      clr_friction = 4.0 * ((100.0 - clr_pct) / 5.0).clip(0, 2.0)   # DILRMP land boundary dispute friction
      rehab_density = 5.0 * (affected_families / 1500.0).clip(0, 1.2) # R&R relocation overhead
      stage_lag = 3.0 * (compensation_deficit > 20.0)             # Milestone lag compensation deficit
      
      target_overrun_pct = clip(delay_escalation + litigation_penalty + clr_friction + rehab_density + stage_lag, 0.0, 50.0)
    """
    delay_days = df["delay_days"].fillna(0).astype(float)
    delay_factor = 10.0 * (delay_days / 365.0).clip(lower=0.0, upper=2.5)
    
    legal_case = df["legal_case"].fillna(0).astype(float)
    legal_factor = 8.0 * legal_case
    
    clr_pct = df["clr_completed_pct"].fillna(97.5).astype(float)
    clr_factor = 4.0 * ((100.0 - clr_pct) / 5.0).clip(lower=0.0, upper=2.0)
    
    families = df["affected_families"].fillna(100).astype(float)
    family_factor = 5.0 * (families / 1500.0).clip(lower=0.0, upper=1.2)
    
    stage_idx = df["stage"].map(lambda s: STAGE_MAP.get(s, 0)).astype(int)
    comp_pct = df["compensation_pct"].fillna(50.0).astype(float)
    stage_lag = np.where((stage_idx >= 3) & (comp_pct < 40.0), 3.5, 0.0)
    
    calc_overrun_pct = (delay_factor + legal_factor + clr_factor + family_factor + stage_lag).clip(lower=0.0, upper=50.0)
    
    # Where historical cost_overrun_pct was documented > 0, honor documented ground truth
    actual_overrun_pct = df["cost_overrun_pct"].fillna(0.0).astype(float)
    final_overrun_pct = np.maximum(actual_overrun_pct.clip(upper=60.0), calc_overrun_pct)
    
    return final_overrun_pct.round(2)

def prepare_cost_features(df: pd.DataFrame) -> pd.DataFrame:
    df_feat = df.copy()
    
    # Defaults
    if "clr_completed_pct" not in df_feat.columns:
        df_feat["clr_completed_pct"] = 97.5
    if "cost_overrun_pct" not in df_feat.columns:
        df_feat["cost_overrun_pct"] = 0.0
    if "legal_case" not in df_feat.columns:
        df_feat["legal_case"] = 0
    if "compensation_pct" not in df_feat.columns:
        df_feat["compensation_pct"] = 50.0
    if "rr_status" not in df_feat.columns:
        df_feat["rr_status"] = "Pending"
    if "stage" not in df_feat.columns:
        df_feat["stage"] = "Section 4 - Preliminary Notification"
    if "budget_crores" not in df_feat.columns:
        df_feat["budget_crores"] = 100.0
    if "affected_families" not in df_feat.columns:
        df_feat["affected_families"] = 100
    if "planned_duration_days" not in df_feat.columns:
        df_feat["planned_duration_days"] = 365
    if "delay_days" not in df_feat.columns:
        df_feat["delay_days"] = 0.0

    # Stage index
    df_feat["stage_index"] = df_feat["stage"].map(lambda s: STAGE_MAP.get(s, 0)).astype(int)
    
    # R&R flags
    df_feat["is_rr_pending"] = (df_feat["rr_status"] == "Pending").astype(int)
    df_feat["is_rr_completed"] = (df_feat["rr_status"] == "Completed").astype(int)
    
    # Legal case
    df_feat["legal_case"] = df_feat["legal_case"].fillna(0).astype(int)
    
    # Expected compensation benchmark
    from backend.app.ml.feature_engineering import EXPECTED_MIN_COMPENSATION_BY_STAGE
    expected_comp = df_feat["stage"].map(lambda s: EXPECTED_MIN_COMPENSATION_BY_STAGE.get(s, 0.0))
    df_feat["compensation_deficit"] = (expected_comp - df_feat["compensation_pct"]).clip(lower=0.0)
    
    # Families per crore
    budget_safe = df_feat["budget_crores"].replace(0, 1.0)
    df_feat["families_per_crore"] = (df_feat["affected_families"] / budget_safe).round(4)
    
    # DILRMP & delay
    df_feat["clr_completed_pct"] = df_feat["clr_completed_pct"].fillna(97.5).astype(float)
    df_feat["delay_days"] = df_feat["delay_days"].fillna(0).astype(float)
    df_feat["planned_duration_days"] = df_feat["planned_duration_days"].fillna(365).astype(float)
    df_feat["affected_families"] = df_feat["affected_families"].fillna(100).astype(float)
    df_feat["compensation_pct"] = df_feat["compensation_pct"].fillna(50.0).astype(float)
    
    # Calculate calibrated risk scores
    risk_scores = []
    for _, row in df_feat.iterrows():
        delay_prob = 1.0 if row["delay_days"] > 60 else (0.7 if row["delay_days"] > 0 else 0.2)
        r = calculate_calibrated_risk_score(
            delay_prob=delay_prob,
            expected_delay_days=row["delay_days"],
            legal_case=int(row["legal_case"]),
            compensation_pct=float(row["compensation_pct"]),
            stage=str(row["stage"]),
            affected_families=int(row["affected_families"])
        )
        risk_scores.append(r["risk_score"])
        
    df_feat["risk_score"] = risk_scores
    
    return df_feat[COST_FEATURE_COLUMNS]

def train_cost_model():
    models_dir = os.path.join(BASE_DIR, "backend", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    data_path = os.path.join(BASE_DIR, "backend", "data", "processed", "clean_data.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
        
    df = pd.read_csv(data_path)
    print(f"[Cost Model] Loaded {len(df)} projects from {data_path}")
    
    X = prepare_cost_features(df)
    y_overrun_pct = derive_target_overrun_pct(df)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_overrun_pct, test_size=0.20, random_state=42
    )
    
    print(f"[Cost Model] Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    reg = RandomForestRegressor(
        n_estimators=120,
        max_depth=6,
        min_samples_split=4,
        random_state=42
    )
    reg.fit(X_train, y_train)
    
    y_pred = reg.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"[Cost Model Overrun Metrics] RMSE: {rmse:.2f}% | MAE: {mae:.2f}% | R2: {r2:.4f}")
    
    # Save artifacts
    cost_model_path = os.path.join(models_dir, "cost_regressor.pkl")
    cost_meta_path = os.path.join(models_dir, "cost_feature_metadata.pkl")
    
    joblib.dump(reg, cost_model_path)
    joblib.dump({
        "feature_columns": COST_FEATURE_COLUMNS,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "rmse_pct": round(float(rmse), 2),
        "mae_pct": round(float(mae), 2),
        "r2_score": round(float(r2), 4)
    }, cost_meta_path)
    
    print(f"[Cost Model] Successfully saved model to {cost_model_path}")
    return reg, {
        "rmse": rmse,
        "mae": mae,
        "r2": r2
    }

if __name__ == "__main__":
    train_cost_model()

