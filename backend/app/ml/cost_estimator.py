import os
import sys
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from backend.app.ml.train_cost_model import prepare_cost_features, COST_FEATURE_COLUMNS
except ImportError:
    from train_cost_model import prepare_cost_features, COST_FEATURE_COLUMNS

class CostEstimator:
    def __init__(self):
        models_dir = os.path.join(BASE_DIR, "backend", "models")
        cost_model_path = os.path.join(models_dir, "cost_regressor.pkl")
        
        if not os.path.exists(cost_model_path):
            from backend.app.ml.train_cost_model import train_cost_model
            train_cost_model()
            
        self.model = joblib.load(cost_model_path)
        
    def estimate_project_cost(self, project_dict: dict) -> Dict[str, Any]:
        """
        Estimates total final expenditure and overrun for a single project.
        """
        df = pd.DataFrame([project_dict])
        X = prepare_cost_features(df)
        
        predicted_overrun_pct = float(self.model.predict(X)[0])
        # Overrun percentage cannot be negative for sanctioned capital works under risk
        predicted_overrun_pct = max(0.0, round(predicted_overrun_pct, 2))
        
        budget = float(project_dict.get("budget_crores", 0.0) or 0.0)
        overrun_crores = round(budget * (predicted_overrun_pct / 100.0), 2)
        estimated_total_cost = round(budget + overrun_crores, 2)
        
        # Color coding and status tier
        if predicted_overrun_pct > 20.0:
            tier = "High Overrun"
            badge = "CRITICAL OVERRUN"
            color = "#EF4444" # Red
        elif predicted_overrun_pct > 5.0:
            tier = "Moderate Overrun"
            badge = "MODERATE OVERRUN"
            color = "#F59E0B" # Amber
        else:
            tier = "On Budget"
            badge = "LOW OVERRUN"
            color = "#10B981" # Green
            
        # Determine top 2-3 driving factors
        factors = []
        delay = float(project_dict.get("delay_days", 0) or 0)
        legal = int(project_dict.get("legal_case", 0) or 0)
        clr = float(project_dict.get("clr_completed_pct", 97.5) or 97.5)
        families = int(project_dict.get("affected_families", 0) or 0)
        comp_pct = float(project_dict.get("compensation_pct", 50.0) or 50.0)
        rr_status = str(project_dict.get("rr_status", "Pending"))
        
        if legal == 1:
            factors.append({
                "factor": "Active Court Litigation",
                "impact": "High statutory interest and legal standstill costs (+10% to 15%)",
                "badge": "Litigation Risk"
            })
        if delay >= 120:
            factors.append({
                "factor": f"Forecasted Acquisition Delay ({int(delay)} Days)",
                "impact": f"Carrying cost inflation and price index escalation across {int(delay)} days delay",
                "badge": "Timeline Slip"
            })
        if clr < 96.0:
            factors.append({
                "factor": f"Sub-Optimal Land Digitization ({clr:.1f}% DILRMP)",
                "impact": "Boundary dispute verification lag pushing administrative overheads",
                "badge": "DILRMP Friction"
            })
        if families >= 1500 or rr_status == "Pending":
            factors.append({
                "factor": f"High Displacement Impact ({families} Families)",
                "impact": "RFCTLARR 2013 Schedule II rehabilitation package and annuity commitments",
                "badge": "R&R Footprint"
            })
        if comp_pct < 35.0:
            factors.append({
                "factor": f"Low Compensation Disbursal ({comp_pct:.1f}%)",
                "impact": "Pending award deposits vulnerable to 100% solatium recalculation",
                "badge": "Disbursal Lag"
            })
            
        if not factors:
            factors.append({
                "factor": "Milestone & Compensation Alignment",
                "impact": "Project compensation progress is on schedule with minimal baseline overrun",
                "badge": "On Track"
            })
            
        # Explanatory summary text
        top_driver_names = [f["factor"] for f in factors[:2]]
        if predicted_overrun_pct > 5.0:
            explanation_summary = f"{' and '.join(top_driver_names)} are pushing estimated total expenditure +{predicted_overrun_pct:.1f}% above sanctioned budget."
        else:
            explanation_summary = "Project parameters indicate expenditure will remain largely within the sanctioned budget limit."
            
        return {
            "project_id": project_dict.get("project_id"),
            "project_name": project_dict.get("project_name"),
            "state": project_dict.get("state"),
            "sector": project_dict.get("sector", "Infrastructure"),
            "stage": project_dict.get("stage"),
            "sanctioned_budget_crores": budget,
            "estimated_total_cost_crores": estimated_total_cost,
            "estimated_overrun_crores": overrun_crores,
            "estimated_overrun_pct": predicted_overrun_pct,
            "overrun_tier": tier,
            "badge": badge,
            "color_code": color,
            "explanation_summary": explanation_summary,
            "top_driving_factors": factors[:3]
        }

    def batch_estimate_costs(self, project_dicts: List[dict]) -> List[Dict[str, Any]]:
        """
        Fast batch estimation for all projects in portfolio.
        """
        if not project_dicts:
            return []
        df = pd.DataFrame(project_dicts)
        X = prepare_cost_features(df)
        preds = np.maximum(0.0, self.model.predict(X))
        
        results = []
        for p, pred_overrun in zip(project_dicts, preds):
            budget = float(p.get("budget_crores", 0.0) or 0.0)
            overrun_pct = round(float(pred_overrun), 2)
            overrun_crores = round(budget * (overrun_pct / 100.0), 2)
            total_cost = round(budget + overrun_crores, 2)
            
            if overrun_pct > 20.0:
                tier = "High Overrun"
                badge = "CRITICAL OVERRUN"
                color = "#EF4444"
            elif overrun_pct > 5.0:
                tier = "Moderate Overrun"
                badge = "MODERATE OVERRUN"
                color = "#F59E0B"
            else:
                tier = "On Budget"
                badge = "LOW OVERRUN"
                color = "#10B981"
                
            delay = float(p.get("delay_days", 0) or 0)
            legal = int(p.get("legal_case", 0) or 0)
            clr = float(p.get("clr_completed_pct", 97.5) or 97.5)
            families = int(p.get("affected_families", 0) or 0)
            
            factors = []
            if legal == 1:
                factors.append("Active Court Litigation (+12% statutory penalty)")
            if delay >= 120:
                factors.append(f"Forecasted Delay of {int(delay)} Days (Inflation impact)")
            if clr < 96.0:
                factors.append(f"State Land Records Digitization lag ({clr:.1f}%)")
            if families >= 1500:
                factors.append(f"High Displaced Population Footprint ({families} families)")
            if not factors:
                factors.append("Timely milestone progression within budget limits")
                
            summary = f"{factors[0]} driving estimated cost." if factors else "Expenditure on schedule."
            
            results.append({
                "project_id": p.get("project_id"),
                "project_name": p.get("project_name"),
                "state": p.get("state"),
                "sector": p.get("sector", "Infrastructure"),
                "stage": p.get("stage"),
                "sanctioned_budget_crores": budget,
                "estimated_total_cost_crores": total_cost,
                "estimated_overrun_crores": overrun_crores,
                "estimated_overrun_pct": overrun_pct,
                "overrun_tier": tier,
                "badge": badge,
                "color_code": color,
                "explanation_summary": summary,
                "top_driving_factors": factors[:3]
            })
        return results

# Singleton instance
_cost_estimator = None

def get_cost_estimator() -> CostEstimator:
    global _cost_estimator
    if _cost_estimator is None:
        _cost_estimator = CostEstimator()
    return _cost_estimator

