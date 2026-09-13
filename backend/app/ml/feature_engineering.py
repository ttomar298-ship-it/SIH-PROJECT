import pandas as pd
import numpy as np

# Canonical stage ordering and typical standard durations (in days)
STAGE_MAP = {
    "Section 4 - Preliminary Notification": 0,
    "Social Impact Assessment (SIA)": 1,
    "Section 11 Notification": 2,
    "Section 19 Declaration (R&R Scheme)": 3,
    "Award of Compensation (Section 23/30)": 4,
    "Possession & Physical Transfer": 5,
}

EXPECTED_MIN_COMPENSATION_BY_STAGE = {
    "Section 4 - Preliminary Notification": 0.0,
    "Social Impact Assessment (SIA)": 5.0,
    "Section 11 Notification": 20.0,
    "Section 19 Declaration (R&R Scheme)": 40.0,
    "Award of Compensation (Section 23/30)": 70.0,
    "Possession & Physical Transfer": 90.0,
}

FEATURE_COLUMNS = [
    "planned_duration_days",
    "compensation_pct",
    "legal_case",
    "affected_families",
    "budget_crores",
    "stage_index",
    "is_rr_pending",
    "is_rr_completed",
    "compensation_deficit",
    "families_per_crore",
    "compensation_bucket_low",
    "compensation_bucket_medium",
    "compensation_bucket_high",
    "stage_overdue_flag",
    "clr_completed_pct",
    "cost_overrun_pct",
    "low_clr_risk_flag",
]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw/clean project dataframe into engineered numerical feature vectors.
    """
    df = df.copy()
    
    # Stage index
    df["stage_index"] = df["stage"].map(lambda s: STAGE_MAP.get(s, 0)).astype(int)
    
    # R&R flags
    df["is_rr_pending"] = (df["rr_status"] == "Pending").astype(int)
    df["is_rr_completed"] = (df["rr_status"] == "Completed").astype(int)
    
    # Legal case flag
    df["legal_case"] = df["legal_case"].fillna(0).astype(int)
    
    # Expected compensation benchmark for the current stage
    expected_comp = df["stage"].map(lambda s: EXPECTED_MIN_COMPENSATION_BY_STAGE.get(s, 0.0))
    # Deficit is positive if current compensation is behind the expected stage minimum
    df["compensation_deficit"] = (expected_comp - df["compensation_pct"]).clip(lower=0.0)
    
    # Families per crore ratio (density of rehabilitation impact)
    df["budget_crores"] = df["budget_crores"].replace(0, 1.0)
    df["families_per_crore"] = (df["affected_families"] / df["budget_crores"]).round(4)
    
    # Compensation buckets
    df["compensation_bucket_low"] = (df["compensation_pct"] < 35.0).astype(int)
    df["compensation_bucket_medium"] = ((df["compensation_pct"] >= 35.0) & (df["compensation_pct"] < 75.0)).astype(int)
    df["compensation_bucket_high"] = (df["compensation_pct"] >= 75.0).astype(int)
    
    # Stage overdue flag
    df["stage_overdue_flag"] = (
        ((df["stage_index"] >= 3) & (df["compensation_pct"] < 40.0)) |
        ((df["stage_index"] >= 2) & (df["legal_case"] == 1) & (df["is_rr_pending"] == 1))
    ).astype(int)
    
    # DILRMP Land Record Digitalization % & Cost Overrun
    df["clr_completed_pct"] = df["clr_completed_pct"].fillna(97.5).astype(float)
    df["cost_overrun_pct"] = df["cost_overrun_pct"].fillna(0.0).astype(float)
    df["low_clr_risk_flag"] = (df["clr_completed_pct"] < 95.0).astype(int)
    
    # Fill any null values
    df["planned_duration_days"] = df["planned_duration_days"].fillna(365)
    df["affected_families"] = df["affected_families"].fillna(100)
    
    return df[FEATURE_COLUMNS]

def engineer_single_project(proj_dict: dict) -> pd.DataFrame:
    """
    Helper to engineer features for a single project dictionary.
    """
    df = pd.DataFrame([proj_dict])
    return engineer_features(df)

