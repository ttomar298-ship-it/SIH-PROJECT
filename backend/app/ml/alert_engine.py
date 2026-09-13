from typing import Dict, Any, List
from datetime import datetime

def evaluate_project_alert(project: dict, risk_score: int, expected_delay_days: float) -> Dict[str, Any]:
    """
    Evaluates a project against risk and delay thresholds to generate alerts.
    """
    alerts = []
    severity = "LOW"
    alert_triggered = False

    # Check Critical Risk Threshold
    if risk_score >= 70:
        severity = "CRITICAL"
        alert_triggered = True
        alerts.append("CRITICAL: Overall project delay risk exceeds 70/100 threshold.")
    elif risk_score >= 50:
        severity = "WARNING"
        alert_triggered = True
        alerts.append("WARNING: Elevated project delay risk detected (>50/100).")

    # Specific Bottleneck Triggers
    if project.get("legal_case") == 1:
        alerts.append("LEGAL: High Court / Tribunal litigation active; physical possession blocked.")
        if severity != "CRITICAL":
            severity = "WARNING"
            alert_triggered = True

    comp_pct = project.get("compensation_pct", 0)
    stage = project.get("stage", "")
    if comp_pct < 30.0 and stage in [
        "Section 19 Declaration (R&R Scheme)",
        "Award of Compensation (Section 23/30)",
        "Possession & Physical Transfer"
    ]:
        alerts.append(f"FINANCIAL: Compensation disbursal severely deficient at {comp_pct}% for stage '{stage}'.")
        alert_triggered = True

    if project.get("rr_status") == "Pending" and project.get("affected_families", 0) > 500:
        alerts.append(f"REHABILITATION: Resettlement pending for {project.get('affected_families')} families.")
        alert_triggered = True

    if expected_delay_days > 90:
        alerts.append(f"SCHEDULE: Expected delay forecast exceeds 3 months (+{int(expected_delay_days)} days).")
        alert_triggered = True

    return {
        "alert_triggered": alert_triggered,
        "severity": severity,
        "risk_score": risk_score,
        "project_id": project.get("project_id"),
        "project_name": project.get("project_name"),
        "state": project.get("state"),
        "district": project.get("district"),
        "alert_count": len(alerts),
        "alert_messages": alerts,
        "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def scan_all_projects_for_alerts(projects: List[dict], risk_scores: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scans a collection of projects and returns all active warnings and critical alerts.
    """
    active_alerts = []
    for proj in projects:
        p_id = proj.get("project_id")
        risk_info = risk_scores.get(p_id, {"risk_score": 0, "expected_delay_days": 0})
        alert_data = evaluate_project_alert(
            proj,
            risk_info.get("risk_score", 0),
            risk_info.get("expected_delay_days", 0)
        )
        if alert_data["alert_triggered"]:
            active_alerts.append(alert_data)
            
    # Sort alerts: CRITICAL first, then highest risk score
    active_alerts.sort(key=lambda a: (0 if a["severity"] == "CRITICAL" else 1, -a["risk_score"]))
    return active_alerts

