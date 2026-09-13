from typing import Dict, Any

def calculate_calibrated_risk_score(
    delay_prob: float,
    expected_delay_days: float,
    legal_case: int = 0,
    compensation_pct: float = 50.0,
    stage: str = "",
    affected_families: int = 0
) -> Dict[str, Any]:
    """
    Computes a calibrated Risk Score (1-100) combining classification probability,
    regression severity (expected delay days), and high-impact contextual risk factors.
    """
    # 1. Base probability contribution (0 to 50 points)
    prob_score = delay_prob * 50.0

    # 2. Expected delay severity contribution (0 to 30 points)
    # 180+ days is considered maximum severity
    severity_ratio = min(1.0, max(0.0, expected_delay_days / 180.0))
    severity_score = severity_ratio * 30.0

    # 3. Contextual modifiers (0 to 20 points)
    context_score = 0.0
    if legal_case == 1:
        context_score += 10.0
    if compensation_pct < 35.0:
        context_score += 6.0
    if affected_families > 1000:
        context_score += 4.0

    raw_score = prob_score + severity_score + context_score
    calibrated_score = int(round(max(1.0, min(100.0, raw_score))))

    if calibrated_score >= 70:
        category = "High"
        color = "#EF4444" # Red
        badge = "CRITICAL"
        action_recommendation = "Immediate district collector intervention required. Fast-track legal settlement and disbursement."
    elif calibrated_score >= 40:
        category = "Medium"
        color = "#F59E0B" # Amber/Orange
        badge = "MODERATE"
        action_recommendation = "Monitor R&R milestones closely. Ensure compensation disbursal meets target schedule."
    else:
        category = "Low"
        color = "#10B981" # Green
        badge = "NORMAL"
        action_recommendation = "Project progress is on track with low likelihood of delay."

    return {
        "risk_score": calibrated_score,
        "risk_category": category,
        "color_code": color,
        "badge": badge,
        "action_recommendation": action_recommendation,
        "components": {
            "probability_component": round(prob_score, 1),
            "severity_component": round(severity_score, 1),
            "context_component": round(context_score, 1)
        }
    }

