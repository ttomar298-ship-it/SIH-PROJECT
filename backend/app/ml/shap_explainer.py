import os
import sys
import joblib
import numpy as np
import pandas as pd
import shap
from typing import List, Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.ml.feature_engineering import FEATURE_COLUMNS, engineer_single_project

FEATURE_LABELS = {
    "planned_duration_days": "Planned Timeline Duration",
    "compensation_pct": "Compensation Disbursed %",
    "legal_case": "Active Court Case / Litigation",
    "affected_families": "Number of Affected Families",
    "budget_crores": "Project Budget",
    "stage_index": "Current Acquisition Stage",
    "is_rr_pending": "R&R Scheme Pending",
    "is_rr_completed": "R&R Scheme Completed",
    "compensation_deficit": "Compensation Deficit vs Stage",
    "families_per_crore": "Displaced Families per INR Crore",
    "compensation_bucket_low": "Severely Low Compensation (<35%)",
    "compensation_bucket_medium": "Moderate Compensation (35-75%)",
    "compensation_bucket_high": "High Compensation (>75%)",
    "stage_overdue_flag": "Stage Overdue / Milestone Lag",
    "clr_completed_pct": "State Land Records Digitization % (DILRMP)",
    "cost_overrun_pct": "Project Cost Overrun %",
    "low_clr_risk_flag": "Sub-95% Digital Land Records Risk Flag",
}

class ShapExplainer:
    def __init__(self):
        models_dir = os.path.join(BASE_DIR, "backend", "models")
        clf_path = os.path.join(models_dir, "delay_classifier.pkl")
        
        if not os.path.exists(clf_path):
            raise FileNotFoundError(f"Model not found at {clf_path}. Train model first.")
            
        self.model = joblib.load(clf_path)
        self.explainer = shap.TreeExplainer(self.model)

    def explain_project(self, project_dict: dict, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Computes TreeSHAP feature contributions for a single project.
        Returns top contributing factors sorted by absolute magnitude.
        """
        X_df = engineer_single_project(project_dict)
        shap_vals = self.explainer.shap_values(X_df)
        
        # Handle different SHAP output formats across versions (list of arrays, 3D array, or 2D array)
        if isinstance(shap_vals, list):
            # Class 1 (delay) SHAP values
            values = shap_vals[1][0]
        elif isinstance(shap_vals, np.ndarray) and len(shap_vals.shape) == 3:
            values = shap_vals[0, :, 1]
        elif isinstance(shap_vals, np.ndarray) and len(shap_vals.shape) == 2:
            values = shap_vals[0]
        else:
            values = np.array(shap_vals).flatten()

        factors = []
        for feat_name, val, raw_val in zip(FEATURE_COLUMNS, values, X_df.iloc[0]):
            human_label = FEATURE_LABELS.get(feat_name, feat_name)
            val_float = float(val)
            direction = "increases_delay" if val_float > 0 else "reduces_delay"
            
            # Generate human-readable explanation snippet
            if feat_name == "legal_case":
                desc = "Active litigation filed in court" if raw_val == 1 else "No litigation recorded"
            elif feat_name == "compensation_pct":
                desc = f"Disbursed compensation is at {raw_val:.1f}%"
            elif feat_name == "is_rr_pending":
                desc = "Resettlement & Rehabilitation scheme is pending" if raw_val == 1 else "R&R scheme progressing"
            elif feat_name == "stage_overdue_flag":
                desc = "Acquisition milestone severely overdue" if raw_val == 1 else "Milestone timeline intact"
            elif feat_name == "affected_families":
                desc = f"{int(raw_val)} families impacted by land acquisition"
            else:
                desc = f"{human_label} = {raw_val}"

            factors.append({
                "feature": feat_name,
                "label": human_label,
                "shap_value": round(val_float, 4),
                "impact": direction,
                "description": desc,
                "raw_value": float(raw_val)
            })

        # Sort by absolute SHAP magnitude descending
        factors.sort(key=lambda x: abs(x["shap_value"]), reverse=True)
        return factors[:top_k]

# Singleton instance
_explainer_instance = None

def get_shap_explainer() -> ShapExplainer:
    global _explainer_instance
    if _explainer_instance is None:
        _explainer_instance = ShapExplainer()
    return _explainer_instance
