import sys
import os
import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

BASE_URL = "http://127.0.0.1:8000"

def run_e2e_tests():
    print("=== 1. TESTING HEALTH & SYSTEM STATUS ===")
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("  [PASS] /health OK")

    print("\n=== 2. TESTING DASHBOARD PORTFOLIO (A5) ===")
    r = requests.get(f"{BASE_URL}/dashboard-data")
    assert r.status_code == 200
    data = r.json()
    print(f"  [PASS] Loaded {data['total_projects']} projects (Avg Risk: {data['avg_risk_score']}/100, Delayed: {data['delayed_projects_count']})")

    sample_proj = data['projects'][0]
    sample_id = sample_proj['project_id']

    print(f"\n=== 3. TESTING SINGLE PROJECT INSPECTION (A2: {sample_id}) ===")
    r = requests.get(f"{BASE_URL}/projects/{sample_id}")
    assert r.status_code == 200
    p = r.json()
    print(f"  [PASS] Project: {p['project_name']} ({p['district']}, {p['state']}), Stage: {p['stage']}")

    print(f"\n=== 4. TESTING DELAY PREDICTION ENGINE (A3: {sample_id}) ===")
    r = requests.get(f"{BASE_URL}/predict/{sample_id}")
    assert r.status_code == 200
    pred = r.json()
    print(f"  [PASS] Delay Status: {pred['delay_label']}, Expected Delay: {pred['expected_delay_days']} days, Confidence: {pred['confidence_score']}%")

    print(f"\n=== 5. TESTING TREE-SHAP ROOT CAUSE EXPLAINABILITY (A4: {sample_id}) ===")
    r = requests.get(f"{BASE_URL}/risk-score/{sample_id}")
    assert r.status_code == 200
    risk = r.json()
    print(f"  [PASS] Risk Score: {risk['risk_score']}/100 ({risk['risk_category']})")
    for idx, factor in enumerate(risk['top_factors'][:3], 1):
        print(f"         Factor #{idx}: {factor['label']} (SHAP: {factor['shap_value']}) -> {factor['description']}")

    print("\n=== 6. TESTING GEOSPATIAL GIS DATA (A8) ===")
    r = requests.get(f"{BASE_URL}/gis-data")
    assert r.status_code == 200
    gis = r.json()
    print(f"  [PASS] Retrieved {len(gis)} geospatial markers for India Map")

    print("\n=== 7. TESTING PROJECT INGESTION / SIMULATION (A7) ===")
    new_proj = {
        "project_name": "Varanasi-Kolkata High-Speed Logistics Link",
        "state": "Uttar Pradesh",
        "district": "Varanasi",
        "stage": "Section 19 Declaration (R&R Scheme)",
        "start_date": "2024-01-15",
        "target_completion_date": "2025-06-15",
        "planned_duration_days": 517,
        "compensation_pct": 31.0,
        "legal_case": 1,
        "rr_status": "Pending",
        "affected_families": 1100,
        "budget_crores": 980.0,
        "latitude": 25.3176,
        "longitude": 82.9739
    }
    r = requests.post(f"{BASE_URL}/projects", json=new_proj)
    assert r.status_code == 200
    created = r.json()
    created_id = created['project_id']
    print(f"  [PASS] Created project {created_id} (Forecasted Delay: {created['delay_days']} days)")

    print("\n=== 8. TESTING ALERT HUB & EMAIL NOTIFICATION (A6 + Dispatch) ===")
    r = requests.get(f"{BASE_URL}/alerts?threshold=70")
    assert r.status_code == 200
    alerts = r.json()
    print(f"  [PASS] Active critical alerts: {len(alerts)}")

    r = requests.post(f"{BASE_URL}/alerts/send-email/{created_id}?recipient=director.nhai@gov.in")
    assert r.status_code == 200
    email_res = r.json()
    print(f"  [PASS] Email Dispatch: {email_res['message']} (Mode: {email_res['mode']})")

    print("\n=== 9. TESTING DILRMP LAND RECORD MODERNIZATION INTEGRATION ===")
    r = requests.get(f"{BASE_URL}/dilrmp-data")
    assert r.status_code == 200
    dilrmp = r.json()
    assert len(dilrmp) >= 30
    print(f"  [PASS] Retrieved {len(dilrmp)} States & UTs land record statistics")

    print("\n=== 10. TESTING BHOOMI AI BRANDING & AUTH MODULE ===")
    from frontend.streamlit_app.utils.auth import DEMO_USERS, login, LOGO_PATH
    assert os.path.exists(LOGO_PATH), "Bhoomi AI logo file not found in assets!"
    assert "director@gatishakti.gov.in" in DEMO_USERS
    assert "cala@revenue.gov.in" in DEMO_USERS
    assert login("director@gatishakti.gov.in", "admin") is True
    print(f"  [PASS] Verified Bhoomi AI logo at {LOGO_PATH} and verified RBAC authentication for {len(DEMO_USERS)} officer roles")

    print("\n======================================================")
    print("  ALL 10 END-TO-END INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
    print("======================================================")


if __name__ == "__main__":
    run_e2e_tests()

