import sys
import os
import pytest
from fastapi.testclient import TestClient

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.app.main import app

def test_full_api_suite():
    with TestClient(app) as client:
        # 1. Health check
        res = client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("[PASS] /health is OK", flush=True)

        # 2. A1: GET /projects
        res = client.get("/projects")
        assert res.status_code == 200, f"/projects failed: {res.text}"
        projects = res.json()
        assert len(projects) > 0, "No projects returned from /projects"
        sample_id = projects[0]["project_id"]
        print(f"[PASS] A1: GET /projects returned {len(projects)} records. Sample ID: {sample_id}")

        # 3. A2: GET /projects/{project_id}
        res = client.get(f"/projects/{sample_id}")
        assert res.status_code == 200, f"/projects/{sample_id} failed: {res.text}"
        p_detail = res.json()
        assert p_detail["project_id"] == sample_id
        print(f"[PASS] A2: GET /projects/{sample_id} returned valid details")

        # 4. A3: GET /predict/{project_id}
        res = client.get(f"/predict/{sample_id}")
        assert res.status_code == 200, f"/predict/{sample_id} failed: {res.text}"
        pred = res.json()
        assert "delay_flag" in pred
        assert "expected_delay_days" in pred
        assert "confidence_score" in pred
        print(f"[PASS] A3: GET /predict/{sample_id} -> Delay Flag: {pred['delay_flag']}, Expected Days: {pred['expected_delay_days']}")

        # 5. A4: GET /risk-score/{project_id}
        res = client.get(f"/risk-score/{sample_id}")
        assert res.status_code == 200, f"/risk-score/{sample_id} failed: {res.text}"
        risk = res.json()
        assert "risk_score" in risk
        assert "top_factors" in risk
        assert len(risk["top_factors"]) > 0
        print(f"[PASS] A4: GET /risk-score/{sample_id} -> Score: {risk['risk_score']}/100, Top SHAP Factor: {risk['top_factors'][0]['label']}")

        # 6. A5: GET /dashboard-data
        res = client.get("/dashboard-data")
        assert res.status_code == 200, f"/dashboard-data failed: {res.text}"
        dash = res.json()
        assert "total_projects" in dash
        assert "avg_risk_score" in dash
        print(f"[PASS] A5: GET /dashboard-data -> Total: {dash['total_projects']}, Avg Risk: {dash['avg_risk_score']}")

        # 7. A6: GET /alerts
        res = client.get("/alerts?threshold=60")
        assert res.status_code == 200, f"/alerts failed: {res.text}"
        alerts = res.json()
        print(f"[PASS] A6: GET /alerts -> {len(alerts)} alerts active")

        # 8. A7: POST /projects
        new_project_payload = {
            "project_name": "Delhi-Jaipur Super Expressway Node",
            "state": "Rajasthan",
            "district": "Jaipur",
            "stage": "Section 19 Declaration (R&R Scheme)",
            "start_date": "2024-03-01",
            "target_completion_date": "2025-09-01",
            "planned_duration_days": 540,
            "compensation_pct": 28.5,
            "legal_case": 1,
            "rr_status": "Pending",
            "affected_families": 1400,
            "budget_crores": 1250.0,
            "latitude": 26.9124,
            "longitude": 75.7873
        }
        res = client.post("/projects", json=new_project_payload)
        assert res.status_code == 200, f"POST /projects failed: {res.text}"
        created = res.json()
        created_id = created["project_id"]
        assert created_id.startswith("PRJ-")
        print(f"[PASS] A7: POST /projects created project {created_id} with delay_days: {created['delay_days']}")

        # 9. A8: GET /gis-data
        res = client.get("/gis-data")
        assert res.status_code == 200, f"/gis-data failed: {res.text}"
        markers = res.json()
        assert len(markers) > 0
        assert "latitude" in markers[0]
        assert "longitude" in markers[0]
        assert "risk_score" in markers[0]
        print(f"[PASS] A8: GET /gis-data returned {len(markers)} map markers")

        # 10. Email dispatch test
        res = client.post(f"/alerts/send-email/{created_id}")
        assert res.status_code == 200, f"send-email failed: {res.text}"
        email_res = res.json()
        assert email_res["status"] == "success"
        print(f"[PASS] POST /alerts/send-email/{created_id} -> {email_res['message']}")

        # 11. DILRMP Land Records test
        res = client.get("/dilrmp-data")
        assert res.status_code == 200, f"GET /dilrmp-data failed: {res.text}"
        dilrmp = res.json()
        assert len(dilrmp) >= 30, f"Expected >= 30 states/UTs in DILRMP, got {len(dilrmp)}"
        assert "State_UT" in dilrmp[0]
        assert "CLR_Completed_Pct" in dilrmp[0]
        print(f"[PASS] GET /dilrmp-data returned {len(dilrmp)} states and Union Territories")

        # 12. Model Metrics validation test
        res = client.get("/model-metrics")
        assert res.status_code == 200, f"GET /model-metrics failed: {res.text}"
        metrics = res.json()
        assert "classifier" in metrics
        assert "regressor" in metrics
        assert "dataset" in metrics
        assert "roc_auc" in metrics["classifier"]
        assert "accuracy" in metrics["classifier"]
        assert "mae" in metrics["regressor"]
        print(f"[PASS] GET /model-metrics -> Acc: {metrics['classifier']['accuracy']}, ROC-AUC: {metrics['classifier']['roc_auc']}, MAE: {metrics['regressor']['mae']}")

        print("\n==========================================")
        print("ALL 12 API CONTRACT TESTS PASSED PERFECTLY!")
        print("==========================================")


if __name__ == "__main__":
    test_full_api_suite()
