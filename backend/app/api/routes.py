import os
import sys
import joblib
import numpy as np
import pandas as pd
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.db.database import get_db
from backend.app.db.crud import get_projects, get_project_by_id, create_or_update_project
from backend.app.schemas.project_schema import (
    ProjectResponse,
    ProjectCreate,
    PredictionResponse,
    RiskScoreResponse,
    DashboardSummaryResponse,
    AlertResponse,
    GISMarkerResponse
)
from backend.app.ml.feature_engineering import engineer_single_project
from backend.app.ml.risk_scoring import calculate_calibrated_risk_score
from backend.app.ml.shap_explainer import get_shap_explainer
from backend.app.ml.alert_engine import evaluate_project_alert, scan_all_projects_for_alerts
from backend.app.ml.email_service import get_email_service

router = APIRouter()

# Lazy model loaders
_clf = None
_reg = None

def get_models():
    global _clf, _reg
    if _clf is None or _reg is None:
        models_dir = os.path.join(BASE_DIR, "backend", "models")
        clf_path = os.path.join(models_dir, "delay_classifier.pkl")
        reg_path = os.path.join(models_dir, "delay_regressor.pkl")
        if not os.path.exists(clf_path) or not os.path.exists(reg_path):
            raise RuntimeError("Trained models not found. Run backend/app/ml/train.py first.")
        _clf = joblib.load(clf_path)
        _reg = joblib.load(reg_path)
    return _clf, _reg

def run_project_prediction(proj_dict: dict) -> Dict[str, Any]:
    clf, reg = get_models()
    X_feat = engineer_single_project(proj_dict)
    
    # Probabilities & classes
    prob = float(clf.predict_proba(X_feat)[0][1])
    flag = int(clf.predict(X_feat)[0])
    
    # Expected delay
    delay_days = max(0.0, float(reg.predict(X_feat)[0]))
    
    # Confidence is distance from 0.5 decision boundary
    confidence = round(abs(prob - 0.5) * 2.0 * 100.0, 1)
    
    return {
        "delay_flag": flag,
        "delay_label": "Delayed" if flag == 1 else "On Schedule",
        "delay_probability": round(prob, 4),
        "expected_delay_days": round(delay_days, 1),
        "confidence_score": confidence
    }

# A1: List all projects
@router.get("/projects", response_model=List[ProjectResponse])
def read_projects(
    state: Optional[str] = Query(None, description="Filter by state name"),
    stage: Optional[str] = Query(None, description="Filter by acquisition stage"),
    skip: int = 0,
    limit: int = 1000,
    db: Session = Depends(get_db)
):
    projects = get_projects(db, state=state, stage=stage, skip=skip, limit=limit)
    return [p.to_dict() for p in projects]

# A2: Single project full detail
@router.get("/projects/{project_id}", response_model=ProjectResponse)
def read_project(project_id: str, db: Session = Depends(get_db)):
    proj = get_project_by_id(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project with ID '{project_id}' not found.")
    return proj.to_dict()

# A3: Predict delay for project
@router.get("/predict/{project_id}", response_model=PredictionResponse)
def predict_project_delay(project_id: str, db: Session = Depends(get_db)):
    proj = get_project_by_id(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project with ID '{project_id}' not found.")
    
    pred_res = run_project_prediction(proj.to_dict())
    return {
        "project_id": project_id,
        **pred_res
    }

# A4: Risk Score + SHAP Explanation
@router.get("/risk-score/{project_id}", response_model=RiskScoreResponse)
def get_project_risk_score(project_id: str, db: Session = Depends(get_db)):
    proj = get_project_by_id(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project with ID '{project_id}' not found.")
    
    p_dict = proj.to_dict()
    pred_res = run_project_prediction(p_dict)
    risk_data = calculate_calibrated_risk_score(
        delay_prob=pred_res["delay_probability"],
        expected_delay_days=pred_res["expected_delay_days"],
        legal_case=p_dict.get("legal_case", 0),
        compensation_pct=p_dict.get("compensation_pct", 50.0),
        stage=p_dict.get("stage", ""),
        affected_families=p_dict.get("affected_families", 0)
    )

    # Calculate SHAP factors
    explainer = get_shap_explainer()
    shap_factors = explainer.explain_project(p_dict, top_k=5)

    return {
        "project_id": project_id,
        "risk_score": risk_data["risk_score"],
        "risk_category": risk_data["risk_category"],
        "color_code": risk_data["color_code"],
        "badge": risk_data["badge"],
        "action_recommendation": risk_data["action_recommendation"],
        "top_factors": shap_factors,
        "components": risk_data["components"]
    }


def batch_predict_and_score(proj_dicts: List[dict]) -> List[Dict[str, Any]]:
    if not proj_dicts:
        return []
    clf, reg = get_models()
    from backend.app.ml.feature_engineering import engineer_features
    df = pd.DataFrame(proj_dicts)
    X_all = engineer_features(df)
    probs = clf.predict_proba(X_all)[:, 1]
    expected_delays = np.maximum(0.0, reg.predict(X_all))

    results = []
    for p, prob, exp_delay in zip(proj_dicts, probs, expected_delays):
        risk = calculate_calibrated_risk_score(
            delay_prob=float(prob),
            expected_delay_days=float(exp_delay),
            legal_case=p.get("legal_case", 0),
            compensation_pct=p.get("compensation_pct", 50.0),
            stage=p.get("stage", ""),
            affected_families=p.get("affected_families", 0)
        )
        results.append({
            "project": p,
            "delay_probability": float(prob),
            "expected_delay_days": float(exp_delay),
            "delay_flag": 1 if prob >= 0.5 or risk["risk_score"] >= 60 else 0,
            "risk": risk
        })
    return results

# A5: Aggregated dashboard data
@router.get("/dashboard-data", response_model=DashboardSummaryResponse)
def get_dashboard_data(db: Session = Depends(get_db)):
    projects = get_projects(db)
    if not projects:
        return {
            "total_projects": 0,
            "delayed_projects_count": 0,
            "delayed_projects_pct": 0.0,
            "avg_risk_score": 0.0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
            "projects": []
        }

    proj_dicts = [p.to_dict() for p in projects]
    batch_results = batch_predict_and_score(proj_dicts)
    
    enriched_projects = []
    total_risk = 0
    high_count = 0
    medium_count = 0
    low_count = 0
    delayed_count = 0

    for item in batch_results:
        p = item["project"]
        risk = item["risk"]
        score = risk["risk_score"]
        total_risk += score
        
        if score >= 70:
            high_count += 1
        elif score >= 40:
            medium_count += 1
        else:
            low_count += 1
            
        if item["delay_flag"] == 1:
            delayed_count += 1

        p_copy = dict(p)
        p_copy["risk_score"] = score
        p_copy["risk_category"] = risk["risk_category"]
        p_copy["color_code"] = risk["color_code"]
        p_copy["expected_delay_days"] = round(item["expected_delay_days"], 1)
        p_copy["delay_probability"] = round(item["delay_probability"], 3)
        p_copy["delay_flag"] = item["delay_flag"]
        enriched_projects.append(p_copy)

    # Sort projects by risk score descending by default
    enriched_projects.sort(key=lambda x: x["risk_score"], reverse=True)
    n = len(enriched_projects)

    return {
        "total_projects": n,
        "delayed_projects_count": delayed_count,
        "delayed_projects_pct": round((delayed_count / n) * 100.0, 1) if n > 0 else 0.0,
        "avg_risk_score": round(total_risk / n, 1) if n > 0 else 0.0,
        "high_risk_count": high_count,
        "medium_risk_count": medium_count,
        "low_risk_count": low_count,
        "projects": enriched_projects
    }

# A6: List of active alerts
@router.get("/alerts", response_model=List[AlertResponse])
def get_active_alerts(
    threshold: int = Query(70, description="Minimum risk score threshold for alert"),
    db: Session = Depends(get_db)
):
    projects = [p.to_dict() for p in get_projects(db)]
    batch_results = batch_predict_and_score(projects)
    
    risk_dict = {}
    for item in batch_results:
        p_id = item["project"]["project_id"]
        risk_dict[p_id] = {
            "risk_score": item["risk"]["risk_score"],
            "expected_delay_days": item["expected_delay_days"]
        }

    all_alerts = scan_all_projects_for_alerts(projects, risk_dict)
    filtered = [a for a in all_alerts if a["risk_score"] >= threshold or a["severity"] == "CRITICAL"]
    return filtered

# A7: Add / Update project
@router.post("/projects", response_model=ProjectResponse)
def save_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    p_data = payload.model_dump()
    
    # Generate project_id if not provided
    if not p_data.get("project_id"):
        state_code = p_data.get("state", "IN")[:2].upper()
        import random
        p_data["project_id"] = f"PRJ-{state_code}-{random.randint(2000, 9999)}"

    # Run quick prediction to populate delay_days and delay_flag
    pred = run_project_prediction(p_data)
    p_data["delay_days"] = int(round(pred["expected_delay_days"]))
    p_data["delay_flag"] = int(pred["delay_flag"])

    saved = create_or_update_project(db, p_data)
    return saved.to_dict()

# A8: GIS Map data
@router.get("/gis-data", response_model=List[GISMarkerResponse])
def get_gis_data(db: Session = Depends(get_db)):
    projects = [p.to_dict() for p in get_projects(db)]
    batch_results = batch_predict_and_score(projects)
    markers = []
    
    for item in batch_results:
        p = item["project"]
        risk = item["risk"]
        markers.append({
            "project_id": p["project_id"],
            "project_name": p["project_name"],
            "state": p["state"],
            "district": p["district"],
            "stage": p["stage"],
            "latitude": p["latitude"],
            "longitude": p["longitude"],
            "risk_score": risk["risk_score"],
            "risk_category": risk["risk_category"],
            "color_code": risk["color_code"],
            "delay_days": int(round(item["expected_delay_days"])),
            "legal_case": p.get("legal_case", 0),
            "compensation_pct": p.get("compensation_pct", 0.0),
            "sector": p.get("sector", "Infrastructure"),
            "budget_cr": p.get("budget_cr", 0.0),
            "affected_families": p.get("affected_families", 0),
            "rr_status": p.get("rr_status", "In Progress")
        })

    return markers

# Bonus Email dispatch endpoint
@router.post("/alerts/send-email/{project_id}")
def dispatch_email_alert(project_id: str, recipient: Optional[str] = None, db: Session = Depends(get_db)):
    proj = get_project_by_id(db, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")
    
    p_dict = proj.to_dict()
    pred = run_project_prediction(p_dict)
    risk = calculate_calibrated_risk_score(
        delay_prob=pred["delay_probability"],
        expected_delay_days=pred["expected_delay_days"],
        legal_case=p_dict.get("legal_case", 0),
        compensation_pct=p_dict.get("compensation_pct", 50.0),
        stage=p_dict.get("stage", ""),
        affected_families=p_dict.get("affected_families", 0)
    )
    alert_info = evaluate_project_alert(p_dict, risk["risk_score"], pred["expected_delay_days"])
    
    email_service = get_email_service()
    result = email_service.send_high_risk_alert(alert_info, recipient=recipient)
    return result

# Endpoint to get state-by-state DILRMP Land Record Digitalization Status
@router.get("/dilrmp-data")
def get_dilrmp_data():
    csv_path = os.path.join(BASE_DIR, "backend", "data", "raw", "dilrmp_land_records.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="DILRMP dataset not found.")
    df = pd.read_csv(csv_path)
    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        r["State_UT"] = str(row.get("State/UT", ""))
        r["Total_RORs"] = row.get("Total RORs", 0)
        r["Total_Villages"] = row.get("Total No. of Villages", 0)
        r["Villages_CLR_Completed"] = row.get("Villages of CLR Completed (No.)", 0)
        r["CLR_Completed_Pct"] = float(row.get("Villages of CLR Completed (%)", 0.0))
        records.append(r)
    return records

